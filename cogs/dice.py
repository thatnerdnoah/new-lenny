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

    @app_commands.command(name="roll", description="Roll a dice!")
    @app_commands.describe(dice="the dice you want to roll")
    @app_commands.choices(dice=[
        app_commands.Choice(name='d20', value="d20"),
        app_commands.Choice(name='d100', value="d100")
    ])
    async def roll_number(self, interaction: Interaction, dice: app_commands.Choice[str]):
        outer_rand = 0
        if dice.value == "d20":
            outer_rand = 20
        elif dice.value == "d100":
            outer_rand = 100
    
        try:
            rolled_number = rand.randint(1, outer_rand)
            embed = Embed(
                title=f"d{outer_rand} Roll",
                type='rich',
                description=f"**{rolled_number}**",
                color=Colour.red()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(Dice(client))
