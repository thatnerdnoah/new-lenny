from discord import Embed, Colour, app_commands, Interaction
from discord.ext import commands
import random as rand
import time

dice_options = [
    "d4", "d6", "d10", "d12", "d20", "d100", "d10000", "d1000000"
]
dice_choices = [app_commands.Choice(name=dice, value=dice) for dice in dice_options]
dice_cog_cooldowns = {}
SPECIAL_NUMBERS = {69, 420, 42069, 69420, 999999}

def dice_cog_cooldown(seconds: int):
    async def predicate(interaction: Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        if user_id in dice_cog_cooldowns:
            last_used = dice_cog_cooldowns[user_id]
            if current_time - last_used < seconds:
                cooldown_remaining = seconds - (current_time - last_used)
                await interaction.response.send_message(
                    f"You're on cooldown! Try again in {cooldown_remaining:.1f} seconds.",
                    ephemeral=True
                )
                return False

        dice_cog_cooldowns[user_id] = current_time
        return True

    return app_commands.check(predicate)

class Dice(commands.Cog, name="Dice"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize_cog()

    async def cog_load(self) -> None:
        self.initialize_cog()
        
    def initialize_cog(self):
        print("I am ready to roll! (Dice cog loaded)")

    @app_commands.command(name="coin", description="Flip a coin!")
    @app_commands.describe(what_for="What are you flipping the coin for?")
    @app_commands.rename(what_for="for")
    @dice_cog_cooldown(seconds=5)
    async def coin_flip(self, interaction: Interaction, what_for: str = ''):
        try:
            coin = rand.randint(0,1)
            # print("The coin number is", coin) # debug line
            embed = Embed(
                title=f"{what_for} (Coin Flip)" if what_for != '' else "Coin Flip",
                type='rich',
                description=f"Heads!" if coin == 0 else f"Tails!",
                color=Colour.red()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Oops!", ephemeral=True)
            print(e)
            return
    
    @app_commands.command(name="roll", description="Roll a dice!")
    @app_commands.describe(dice="The dice you want to roll")
    @app_commands.describe(what_for="What are you rolling for?")
    @app_commands.rename(what_for="for")
    @app_commands.choices(dice=dice_choices)
    @dice_cog_cooldown(seconds=5)
    async def roll_number(self, interaction: Interaction, dice: str, what_for: str = ''):
        max_roll: int = 0
        if dice.startswith("d"):
            max_roll = int(dice[1:])  # Extract number after 'd'
        else:
            await interaction.response.send_message("Invalid dice selection!", ephemeral=True)
            return
  
        try:
            rolled_number = rand.randint(1, max_roll)
            # Determine color
            if rolled_number == max_roll or rolled_number in SPECIAL_NUMBERS:
                embed_color = Colour.gold()
            else:
                embed_color = Colour.red()
    
            embed = Embed(
                title=f"{what_for} (d{max_roll})" if what_for != '' else f"d{max_roll} Roll",
                type='rich',
                description=f"**{rolled_number}**",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            
    # future implementation of adding special numbers

async def setup(client):
    await client.add_cog(Dice(client))
