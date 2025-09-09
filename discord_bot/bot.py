import os
import logging
from utils.logger import setup_logging
import asyncio
import discord
from discord.ext import commands

# 環境変数の読み込み
from dotenv import load_dotenv
load_dotenv()

setup_logging()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
# message_content は discord.py v2 の場合必要
try:
    intents.message_content = True
except Exception:
    pass

PREFIX = os.getenv('PREFIX', 'mo!')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

COGS = [
    'cogs.moderation',
    'cogs.welcome',
    'cogs.notifications',
    'cogs.admin',
    'cogs.logging'
]


@bot.event
async def on_ready():
    logging.getLogger('bot').info(f'Logged in as {bot.user} (id: {bot.user.id})')
    for guild in bot.guilds:
        logging.getLogger('bot').info(f'Connected to guild: {guild.name} (id: {guild.id})')


async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logging.getLogger('bot').info(f'Loaded cog: {cog}')
        except Exception as e:
            logging.getLogger('bot').exception(f'Failed to load cog {cog}: {e}')


# --- Botの起動 ---
if __name__ == '__main__':
    # ファイル変更時に自動再起動（watchdog使用）
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        import sys
        import time
        class RestartHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                # 除外ディレクトリやファイルを監視しない
                exclude_dirs = ['.venv', '__pycache__']
                if any(ex in event.src_path for ex in exclude_dirs):
                    return
                if event.event_type in ['modified', 'created', 'deleted']:
                    print('File changed, restarting bot...')
                    os.execv(sys.executable, ['python'] + sys.argv)
        observer = Observer()
        # 必要なディレクトリだけ監視（例: cogs, utils, database）
        observer.schedule(RestartHandler(), path='./cogs', recursive=True)
        observer.schedule(RestartHandler(), path='./utils', recursive=True)
        observer.schedule(RestartHandler(), path='./database', recursive=True)
        observer.start()
    except ImportError:
        print('watchdogが未インストールのため自動再起動は無効です')
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        logging.getLogger('bot').error('DISCORD_TOKEN not set in environment')
        raise SystemExit('DISCORD_TOKEN not set')

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(load_cogs())
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logging.getLogger('bot').info('Bot stopped by user (KeyboardInterrupt)')
    finally:
        loop.close()