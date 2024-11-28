import discord
from discord.ext import commands
from discord import app_commands, Interaction

class Ping(commands.Cog, name="ping"):
    """
    This is a test cog for making sure the cog manager works. The only command is to reply a ping command with pong.
    """

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.initialize_cog()

    def initialize_cog(self) -> None:
        print("Ping is ready!")
    
    async def cog_load(self) -> None:
        self.initialize_cog()

    async def cog_unload(self) -> None:
        print("Ping has been unloaded!")

    @app_commands.command(name="ping", description="Ping the bot!")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ping(bot))