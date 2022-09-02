import traceback
import asyncio

from discord import Game, Intents

from discord.ext.commands import Bot

try:
    import config_local as config
except ImportError:
    import config

intents = Intents.default()
intents.message_content = True
    
bot = Bot(command_prefix=config.prefix, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="Escaping Meteor Simulator"))
    print(f"Logged in as {bot.user.name}!")


async def add_extensions():
    await bot.load_extension("cogs.counting")


asyncio.run(add_extensions())
bot.run(config.token)