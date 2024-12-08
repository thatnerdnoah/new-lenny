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

    @commands.Cog.listener()
    async def on_ready(self):
        print("Command Manager has been activated!")
        print("Loading pre-configured cogs...")
        try:
            for cog in config.cogs:
                print(f"Loading {cog}...")
                await self.bot.load_extension(cog)
            print("All pre-configured cogs loaded!")
            await self.sync_commands()
        except Exception as e:
            print(e)

    async def sync_commands(self):
        print("Syncing commands...")
        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")

    @app_commands.command(name="load", description="Load functions into Lenny!")
    @app_commands.describe(cog="The cog you want to load")
    @app_commands.default_permissions(administrator=True)
    async def load_cog_command(self, interaction: Interaction, cog: str) -> None:
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
        try:
            await interaction.response.defer(ephemeral=True)
            success_text = f"The cog {cog} loaded successfully!"
            await self.bot.load_extension(cog)
            await self.sync_commands()
            await interaction.followup.send(success_text)
        except Exception as e:
            await interaction.followup.send("Oops! Something went wrong.")
            print(e)

    @app_commands.command(name="unload", description="Unload any of Lenny's functions!")
    @app_commands.describe(cog="The cog you want to unload")
    @app_commands.default_permissions(administrator=True)
    async def unload_cog_command(self, interaction: Interaction, cog: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
        if "cog_manager" in cog:
            return await interaction.response.send_message("You cannot unload the cog manager. Use the reload command instead!", ephemeral=True)

        try:
            await interaction.response.defer(ephemeral=True)
            success_text: str = f"The cog {cog} was unloaded successfully!"
            await self.bot.unload_extension(cog)
            await self.sync_commands()
            await interaction.followup.send(success_text)
        except Exception as e:
            await interaction.followup.send("Oops! Something went wrong.")
            print(e)

    @app_commands.command(name="reload", description="Reload any of Lenny's functions!")
    @app_commands.describe(cog="The cog/extension to reload")
    @app_commands.default_permissions(administrator=True)
    async def reload_cog_command(self, interaction: Interaction, cog: str):      
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True) 
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            success_text: str = f"The cog {cog} was reloaded successfully!"
            await self.bot.reload_extension(cog)
            await self.sync_commands()
            await interaction.followup.send(success_text)
        except Exception as e:
            await interaction.followup.send("Oops! Something went wrong.")
            print(e)
    
async def setup(client):
    await client.add_cog(CogManager(client))