import re
import time
import logging
from collections import defaultdict, deque

import discord
from discord.ext import commands, tasks

logger = logging.getLogger('moderation')

DEFAULT_SETTINGS = {
    'warn_threshold': 1,
    'delete_threshold': 2,
    'mute_threshold': 3,
    'kick_threshold': 5,
    'mute_duration': 300,  # seconds
    'spam_interval': 5,  # seconds
    'spam_count': 5,
}


class Moderation(commands.Cog):
    """簡易なルールベースの荒らし対策Cog

    - 禁止ワード検知
    - URL検査（ドメインホワイトリスト/ブラックリスト）
    - 短時間連続投稿（スパム）検知
    - 段階的処理：警告→削除→mute→kick/ban
    """

    def __init__(self, bot):
        self.bot = bot
        self.settings = defaultdict(lambda: DEFAULT_SETTINGS.copy())
        # per-guild recent messages for spam detection: guild_id -> user_id -> deque of timestamps
        self.recent = defaultdict(lambda: defaultdict(lambda: deque()))
        # per-guild banned words (in-memory; should be backed by DB)
        self.banned_words = defaultdict(set)
        # simple domain blacklist/whitelist
        self.domain_blacklist = defaultdict(set)
        self.domain_whitelist = defaultdict(set)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return

        guild_id = message.guild.id
        author_id = message.author.id

        # log message to DB: placeholder
        logger.info(f'Message from {message.author} in {message.guild.name}: {message.content}')

        # check banned words
        if self.contains_banned_word(guild_id, message.content):
            await self.handle_infraction(message, reason='banned_word')
            return

        # check URLs
        urls = self.extract_urls(message.content)
        if urls:
            for url in urls:
                domain = self.extract_domain(url)
                if domain in self.domain_blacklist[guild_id]:
                    await self.handle_infraction(message, reason='blacklisted_domain')
                    return
                if self.domain_whitelist[guild_id] and domain not in self.domain_whitelist[guild_id]:
                    await self.handle_infraction(message, reason='unapproved_domain')
                    return

        # spam detection
        now = time.time()
        dq = self.recent[guild_id][author_id]
        dq.append(now)
        # remove old
        while dq and now - dq[0] > self.settings[guild_id]['spam_interval']:
            dq.popleft()
        if len(dq) >= self.settings[guild_id]['spam_count']:
            await self.handle_infraction(message, reason='spam')
            return

    def contains_banned_word(self, guild_id, content):
        msg = content.lower()
        for w in self.banned_words[guild_id]:
            if w in msg:
                return True
        return False

    url_re = re.compile(r'https?://[^\s]+')

    def extract_urls(self, text):
        return self.url_re.findall(text)

    def extract_domain(self, url):
        # very simple domain extractor
        m = re.match(r'https?://([^/]+)', url)
        if m:
            return m.group(1).lower()
        return ''

    async def handle_infraction(self, message, reason='rule_violation'):
        guild_id = message.guild.id
        author = message.author
        settings = self.settings[guild_id]

        # increment warning count in-memory (should persist to DB)
        if not hasattr(author, 'warn_count'):
            setattr(author, 'warn_count', 0)
        author.warn_count += 1

        # log infraction
        logger.info(f'Infraction for {author} in {message.guild.name}: {reason} (warns={author.warn_count})')

        # Decide action based on counts
        if author.warn_count >= settings['kick_threshold']:
            try:
                await message.delete()
            except Exception:
                pass
            await message.guild.kick(author, reason='Auto moderation: threshold exceeded')
            await self.notify_admins(message.guild, f'User {author} kicked for {reason}')
            return

        if author.warn_count >= settings['mute_threshold']:
            # try to add a mute role
            await self.apply_mute(message.guild, author, settings['mute_duration'])
            await self.notify_admins(message.guild, f'User {author} muted for {settings["mute_duration"]}s due to {reason}')
            return

        if author.warn_count >= settings['delete_threshold']:
            try:
                await message.delete()
            except Exception:
                pass
            await message.channel.send(f'{author.mention}, your message was removed. Please follow the server rules. (reason: {reason})')
            return

        # default warn
        await message.channel.send(f'{author.mention}, this is a warning. Reason: {reason}')

    async def apply_mute(self, guild, member, duration):
        # find or create a mute role
        mute_role = None
        for r in guild.roles:
            if r.name.lower() == 'muted':
                mute_role = r
                break
        if not mute_role:
            try:
                mute_role = await guild.create_role(name='Muted', reason='Create mute role for moderation')
                for ch in guild.channels:
                    try:
                        await ch.set_permissions(mute_role, send_messages=False, speak=False)
                    except Exception:
                        pass
            except Exception:
                logger.exception('Failed to create mute role')
                return

        try:
            await member.add_roles(mute_role, reason='Auto mute')
        except Exception:
            logger.exception('Failed to assign mute role')
            return

        # schedule unmute
        self.bot.loop.create_task(self._unmute_later(guild.id, member.id, duration))

    async def _unmute_later(self, guild_id, member_id, duration):
        await asyncio.sleep(duration)
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return
        member = guild.get_member(member_id)
        if not member:
            return
        for r in guild.roles:
            if r.name.lower() == 'muted' and r in member.roles:
                try:
                    await member.remove_roles(r, reason='Auto unmute after duration')
                except Exception:
                    pass

    async def notify_admins(self, guild, message):
        # placeholder: send to guild.owner and any role with administrator
        try:
            if guild.owner:
                await guild.owner.send(message)
        except Exception:
            pass

    # Admin commands to manage settings and banned words
    @commands.group(name='mod', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def mod(self, ctx):
        """Show moderation settings"""
        guild_id = ctx.guild.id
        await ctx.send(f'Moderation settings: {self.settings[guild_id]}')

    @mod.command(name='addword')
    @commands.has_permissions(administrator=True)
    async def add_word(self, ctx, word: str):
        guild_id = ctx.guild.id
        self.banned_words[guild_id].add(word.lower())
        await ctx.send(f'Added banned word: {word}')

    @mod.command(name='removeword')
    @commands.has_permissions(administrator=True)
    async def remove_word(self, ctx, word: str):
        guild_id = ctx.guild.id
        self.banned_words[guild_id].discard(word.lower())
        await ctx.send(f'Removed banned word: {word}')


async def setup(bot):
    await bot.add_cog(Moderation(bot))