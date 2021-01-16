import traceback
import discord

from discord import Game, Streaming, Activity, ActivityType, Guild
from discord.ext import commands

from discord.ext.commands import Bot

import config

bot = Bot(command_prefix=config.prefix)

@bot.event
async def on_ready():
    await bot.change_presense(activity=Game(name="with my dino toys"))
    print(f"Logged in as {bot.user.name}!")


def main():
    for cog in config.cogs:
        try:
            bot.load_extension(cog)
            print(f"Loaded extension {cog}")
        except Exception as error:
            print(f"Cog {cog} could not be loaded. Reason: {error}")
            traceback.print_exc()

    bot.run(config.token)


if __name__ == "__main__":
    main()