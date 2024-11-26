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
    @app_commands.choices(dice=[
        app_commands.Choice(name="d2", value="d2"),
        app_commands.Choice(name="d4", value="d4"),
        app_commands.Choice(name="d6", value="d6"),
        app_commands.Choice(name="d10", value="d10"),
        app_commands.Choice(name='d20', value="d20"),
        app_commands.Choice(name='d100', value="d100")
    ])
    async def roll_number(self, interaction: Interaction, dice: app_commands.Choice[str], what_for: str = ''):
        outer_rand = 0
        if dice.value == "d2":
            outer_rand = 2
        elif dice.value == "d4":
            outer_rand = 4
        elif dice.value == "d6":
            outer_rand = 6
        elif dice.value == "d10":
            outer_rand = 10
        elif dice.value == "d20":
            outer_rand = 20
        elif dice.value == "d100":
            outer_rand = 100
  
        try:
            rolled_number = rand.randint(1, outer_rand)
            embed = Embed(
                title=f"{what_for} (d{outer_rand})" if what_for != '' else f"d{outer_rand} Roll",
                type='rich',
                description=f"**{rolled_number}**",
                color=Colour.red()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(Dice(client))