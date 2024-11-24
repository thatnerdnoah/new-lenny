import asyncio

from discord import Game, Intents

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
        for sync in synced:
            print(f"{sync}")
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        bot.get_channel(config.log_channel).send("The bot didn't load correctly. Check the server!")
        print(e)

@bot.command(name="sync")
async def sync(ctx):
    synced = await bot.tree.sync()
    for sync in synced:
        print(f"{sync}")
    print(f"Synced {len(synced)} command(s).")

async def main():
    async with bot:
        try:
            for cog in config.cogs:
                await bot.load_extension(cog)
        except Exception as e:
            print(e)
        
        await bot.start(config.token)

if __name__ == "__main__":
    asyncio.run(main())