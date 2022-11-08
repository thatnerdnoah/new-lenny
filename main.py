import traceback
import asyncio

from discord import Game, Intents, Interaction

from discord.ext.commands import Bot

try:
    import config_local as config
except ImportError:
    import config

intents = Intents.default()
intents.message_content = True
    
bot = Bot(command_prefix=config.prefix, intents=intents, application_id=config.bot_id)

@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="Escaping Meteor Simulator"))
    print(f"Logged in as {bot.user.name}!")


async def main():
    async with bot:
        await bot.load_extension("cogs.counting")
        await bot.start(config.token)

if __name__ == "__main__":
    asyncio.run(main())