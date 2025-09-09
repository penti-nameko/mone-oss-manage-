import logging
import discord
from discord.ext import commands

logger = logging.getLogger('admin')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Botの情報を表示"""
        await ctx.send(f'Bot is running. Connected to {len(self.bot.guilds)} guild(s).')

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'Kicked {member} ({reason})')
        except Exception:
            logger.exception('Kick failed')
            await ctx.send('Failed to kick member')

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'Banned {member} ({reason})')
        except Exception:
            logger.exception('Ban failed')
            await ctx.send('Failed to ban member')

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: str):
        # member: 'name#discrim'
        bans = await ctx.guild.bans()
        name, discrim = member.split('#')
        for entry in bans:
            user = entry.user
            if user.name == name and user.discriminator == discrim:
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user}')
                return
        await ctx.send('User not found in ban list')


async def setup(bot):
    await bot.add_cog(Admin(bot))