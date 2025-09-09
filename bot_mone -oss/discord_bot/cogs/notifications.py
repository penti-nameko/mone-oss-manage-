import logging
import discord
from discord.ext import commands

logger = logging.getLogger('notifications')

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def notify_guild_admins(self, guild, message):
        # send DM to guild owner and members with administrator permission
        sent = 0
        try:
            if guild.owner:
                await guild.owner.send(message)
                sent += 1
        except Exception:
            pass
        for member in guild.members:
            try:
                if member.guild_permissions.administrator and not member.bot:
                    await member.send(message)
                    sent += 1
            except Exception:
                pass
        logger.info(f'Notified {sent} admins in guild {guild.name}')

    async def notify_channel(self, guild, channel_id, message):
        ch = guild.get_channel(channel_id)
        if ch:
            try:
                await ch.send(message)
            except Exception:
                logger.exception('Failed to send notification to channel')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(YOUR_CHANNEL_ID)
        if channel:
            await channel.send(f'Welcome to the server, {member.mention}!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(YOUR_CHANNEL_ID)
        if channel:
            await channel.send(f'{member.mention} has left the server. We will miss you!')

async def setup(bot):
    await bot.add_cog(Notifications(bot))