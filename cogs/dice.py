from discord import TextChannel, Embed, Colour, app_commands, Interaction
from discord.ext import commands
import random as rand

try:
    import config_local as config
    local_test = True
except ImportError:
    import config

class Dice(commands.Cog, name="Dice"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.dice_channel : TextChannel = None
        self.log_channel : TextChannel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.dice_channel = self.bot.get_channel(config.dice_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)

        print("I am ready to roll! (Dice cog loaded)")

    @app_commands.command(name="roll", description="Roll a D20!")
    async def roll_number(self, interaction: Interaction):
        try:
            rolled_number = rand.randint(1,20)
            embed = Embed(
                title="D20 Roll",
                type='rich',
                color=Colour.purple()
            )
            embed.add_field(name="Rolled number", value=rolled_number)
            await interaction.send_message(f"{rolled_number}")
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(Dice(client))
