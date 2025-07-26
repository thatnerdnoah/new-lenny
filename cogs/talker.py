from discord import TextChannel, Embed, Colour, app_commands, Interaction
from discord.ext import commands
from cogs.cog_manager import command_cooldown

class Talker(commands.Cog, name="Talker"):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize_cog()
    
    async def cog_load(self):
        self.initialize_cog()

    def initialize_cog(self):
        print("You can talk as me now! (Talker cog loaded)")
    
    @app_commands(name="talker", description="Send a message in a channel as Lenny!")
    @app_commands.describe(
        message="What would you like Lenny to say?",
        channel="What channel should Lenny message in?"
    )
    @app_commands.default_permissions(administrator=True)
    @command_cooldown(seconds=5)
    async def send_message(self, interaction: Interaction, message: str, channel: TextChannel):
        if not message:
            await interaction.response.send_message("You need to send a message!", ephemeral=True)
            return
        
        try:
            await channel.send(message)
            await interaction.response.send_message(f"✅ Message has been sent!")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failure to send message: {e}", ephemeral=True)

async def setup(client):
    await client.add_cog(Talker(client))