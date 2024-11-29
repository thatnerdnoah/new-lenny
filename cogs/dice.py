from discord import TextChannel, Embed, Colour, app_commands, Interaction
from discord.ext import commands
import random as rand

try:
    import config_local as config
    local_test = True
except ImportError:
    import config

dice_options = [
    "d2", "d4", "d6", "d10", "d20", "d100", "d1000", "d10000", "d100000", "the million"
]
dice_choices = [app_commands.Choice(name=dice, value=dice) for dice in dice_options]

class Dice(commands.Cog, name="Dice"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        # self.dice_channel : TextChannel = None
        # self.log_channel : TextChannel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize_cog()

    async def cog_load(self) -> None:
        self.initialize_cog()
        
    def initialize_cog(self):
        self.dice_channel = self.bot.get_channel(config.dice_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)
        print("I am ready to roll! (Dice cog loaded)")

    @app_commands.command(name="roll", description="Roll a dice!")
    @app_commands.describe(dice="The dice you want to roll")
    @app_commands.describe(what_for="What are you rolling for?")
    @app_commands.rename(what_for="for")
    @app_commands.choices(dice=dice_choices)
    async def roll_number(self, interaction: Interaction, dice: str, what_for: str = ''):
        max_roll = 0
        if dice.startswith("d"):
            max_roll = int(dice[1:])  # Extract number after 'd'
        elif dice == "the million":
            max_roll = 1000000
        else:
            await interaction.response.send_message("Invalid dice selection!", ephemeral=True)
            return
  
        try:
            rolled_number = rand.randint(1, max_roll)
            embed = Embed(
                title=f"{what_for} (d{max_roll})" if what_for != '' else f"d{max_roll} Roll",
                type='rich',
                description=f"**{rolled_number}**",
                color=Colour.red()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(Dice(client))
