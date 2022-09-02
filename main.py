import traceback

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


async def main():
    for cog in config.cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded extension {cog}")
        except Exception as error:
            print(f"Cog {cog} could not be loaded. Reason: {error}")
            traceback.print_exc()

    bot.run(config.token)


if __name__ == "__main__":
    main()