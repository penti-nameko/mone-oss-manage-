import logging
import discord
from discord.ext import commands

logger = logging.getLogger('welcome')

DEFAULT_WELCOME = "Welcome to {guild}, {member}!"
DEFAULT_LEAVE = "Goodbye {member} from {guild}."


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # per-guild welcome config
        self.configs = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        cfg = self.configs.get(guild.id, {})
        channel_id = cfg.get('channel_id')
        message = cfg.get('welcome_message', DEFAULT_WELCOME)
        if channel_id:
            ch = guild.get_channel(channel_id)
            if ch:
                try:
                    await ch.send(message.format(guild=guild.name, member=member.mention))
                except Exception:
                    logger.exception('Failed to send welcome message')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        cfg = self.configs.get(guild.id, {})
        channel_id = cfg.get('channel_id')
        message = cfg.get('leave_message', DEFAULT_LEAVE)
        if channel_id:
            ch = guild.get_channel(channel_id)
            if ch:
                try:
                    await ch.send(message.format(guild=guild.name, member=member.name))
                except Exception:
                    logger.exception('Failed to send leave message')

    @commands.group(name='welcome', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        cfg = self.configs.get(ctx.guild.id, {})
        await ctx.send(f'Current welcome config: {cfg}')

    @welcome.command(name='set')
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel, *, message: str):
        gid = ctx.guild.id
        self.configs.setdefault(gid, {})
        self.configs[gid]['channel_id'] = channel.id
        self.configs[gid]['welcome_message'] = message
        await ctx.send(f'Welcome message set for {channel.mention}')

    @welcome.command(name='setleave')
    @commands.has_permissions(administrator=True)
    async def set_leave(self, ctx, channel: discord.TextChannel, *, message: str):
        gid = ctx.guild.id
        self.configs.setdefault(gid, {})
        self.configs[gid]['channel_id'] = channel.id
        self.configs[gid]['leave_message'] = message
        await ctx.send(f'Leave message set for {channel.mention}')


async def setup(bot):
    await bot.add_cog(Welcome(bot))