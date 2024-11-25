import discord
from discord.ext import commands
from discord import app_commands, Interaction

try:
    import config_local as config
    local_test = True
except ImportError:
    import config

class CogManager(commands.Cog, name="CogManager"):
    """
    This cog allows for the loading and unloading of cogs. This cog cannot be unloaded.
    """
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.guild = 0
        self.cogs = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Command Manager has been activated!")
        print("Loading pre-configured cogs...")
        try:
            for cog in config.cogs:
                await self.load_cog(cog=cog, silent=True)
                self.cogs.append(cog)
            print("All pre-configured cogs loaded!")
        except Exception as e:
            print(e)

    async def load_cog(self, cog: str, silent: bool = False):
        await self.bot.load_extension(cog)
    
    async def unload_cog(self, cog: str, silent: bool = False) -> None:
        await self.bot.unload_extension(cog)

    async def reload_cog(self, interaction: Interaction):
        await self.unload_cog(self, interaction, silent=True)
        await self.load_cog(self, interaction, silent=True)

    @app_commands.command(name="load_cog")
    async def load_cog_command(self, interaction: Interaction, cog: str, silent: bool) -> None:
        success_text = f"The cog {cog} loaded successfully!"
        await self.load_cog(interaction, cog)
        await interaction.response.send_message(success_text, ephemeral=True) if not silent else print(success_text)

    @app_commands.command(name="unload_cog")
    async def unload_cog_command(self, interaction: Interaction, cog: str, silent: bool = False):
        success_text: str = f"The cog {cog} was unloaded successfully!"
        await self.unload_cog(interaction, cog)
        await interaction.response.send_message(success_text, ephemeral=True) if not silent else print(success_text)

    
    


async def setup(client):
    await client.add_cog(CogManager(client))