import traceback
import asyncio

from discord import Game, Intents, app_commands

from discord.ext.commands import Bot

try:
    import config_local as config
except ImportError:
    import config

intents = Intents.default()
intents.message_content = True
    
bot = Bot(command_prefix='$', intents=intents, application_id=config.bot_id)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")
    try:
        await bot.change_presence(activity=Game(name="Escaping Meteor Simulator"))
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        bot.get_channel(config.log_channel).send("The bot didn't load correctly. Check the server!")
        print(e)

async def main():
    async with bot:
        await bot.load_extension("cogs.counting")
        await bot.start(config.token)

if __name__ == "__main__":
    asyncio.run(main())