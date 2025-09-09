import logging
import time

import discord
from discord.ext import commands

logger = logging.getLogger('cog_logging')

class CogLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # Here you would insert the message into DB via database/db_manager.py
        logger.info(f'Log message: guild={getattr(message.guild, "id", None)} user={message.author} content={message.content[:100]}')

    async def log_moderation_action(self, guild_id, user_id, action, reason=None):
        # placeholder to persist moderation actions
        logger.info(f'ModerationLog guild={guild_id} user={user_id} action={action} reason={reason}')


async def setup(bot):
    await bot.add_cog(CogLogging(bot))

class DiscordLogger:
    def __init__(self):
        self.logger = logging.getLogger("DiscordBot")
        self.logger.setLevel(logging.INFO)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add handler to the logger
        self.logger.addHandler(ch)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

# Example usage
if __name__ == "__main__":
    logger = DiscordLogger()
    logger.log_info("Logging system initialized.")