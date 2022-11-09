import asyncio
import config
import discord
from discord import app_commands
from discord.ext.commands import Bot

MY_GUILD = discord.Object(id=0)

class LennyStandard(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

# class LennyExt(Bot):
#     def __init__(self, *, intents: discord.Intents) -> None:
#         super().__init__(command_prefix='/', intents=intents, application_id=config.bot_id)


intents = discord.Intents.default()
client = Lenny(intents=intents)

@client.event
async def on_ready():
    await bot.change_presence(activity=Game(name="Escaping Meteor Simulator"))
    print(f"Logged in as {bot.user.name}!")
    print('--------')

async def main():
    async with client:
        await client.add_cog("cogs.counting")
        await client.run(config.token)

asyncio.run(main())