### Cog for creating and managing counters in Discord channels.

from discord import TextChannel, Embed, Colour, app_commands, Interaction
from discord.ext import commands
from datetime import datetime

import discord

class CounterButtonView(discord.ui.View):
    def __init__(self, counters: dict, channel_id, name: str):
        super().__init__(timeout=None)
        self.counters = counters
        self.channel_id = channel_id
        self.name = name

    def value(self) -> int:
        return self.counters[self.channel_id][self.name]

    async def update(self, interaction: Interaction):
        await interaction.response.edit_message(
            content=f"📊 **Counter `{self.name}`**\nCurrent value: **{self.value()}**",
            view=self
        )

    @discord.ui.button(label="+1", style=discord.ButtonStyle.success)
    async def increment(self, interaction: Interaction, button: discord.ui.Button):
        self.counters[self.channel_id][self.name] += 1
        await self.update(interaction)

    @discord.ui.button(label="-1", style=discord.ButtonStyle.danger)
    async def decrement(self, interaction: Interaction, button: discord.ui.Button):
        self.counters[self.channel_id][self.name] -= 1
        await self.update(interaction)


class Counter(commands.Cog):
    """A cog for creating and managing counters in Discord channels."""

    def __init__(self, bot):
        self.bot = bot
        self.counters = {}  # Dictionary to store counters for each channel

    # TODO: Experiment with button functionality for incrementing/decrementing counters without needing to type commands
    
    async def cog_load(self) -> None:
        await self.initialize_cog()

    async def initialize_cog(self) -> None:
        print("Counter cog loaded and initialized.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.initialize_cog()

    @app_commands.command(name='createcounter', description='Creates a new counter with the given name.')
    @app_commands.describe(name='The name of the counter to create.')
    @app_commands.describe(starting_value='The starting value of the counter (default is 0).')
    async def create_counter(self, interaction: Interaction, name: str, starting_value: int = 0):
        """Creates a new counter with the given name."""
        channel_id = interaction.channel_id
        if channel_id not in self.counters:
            self.counters[channel_id] = {}
        if name in self.counters[channel_id]:
            await interaction.response.send_message(f"A counter named '{name}' already exists in this channel.")
            return
        self.counters[channel_id][name] = starting_value
        await interaction.response.send_message(f"Counter '{name}' created with initial value of {starting_value}.")

    @app_commands.command(name='increment', description='Increments the specified counter by 1.')
    @app_commands.describe(name='The name of the counter to increment.')
    async def increment_counter(self, interaction: Interaction, name: str):
        """Increments the specified counter by 1."""
        channel_id = interaction.channel_id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await interaction.response.send_message(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] += 1
        await interaction.response.send_message(f"Counter '{name}' incremented. Current value: {self.counters[channel_id][name]}")
        
    @app_commands.command(name='decrement', description='Decrements the specified counter by 1.')
    @app_commands.describe(name='The name of the counter to decrement.')
    async def decrement_counter(self, interaction: Interaction, name: str):
        """Decrements the specified counter by 1."""
        channel_id = interaction.channel_id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await interaction.response.send_message(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] -= 1
        await interaction.response.send_message(f"Counter '{name}' decremented. Current value: {self.counters[channel_id][name]}")
    
    @app_commands.command(name='resetcounter', description='Resets the specified counter to 0.')
    @app_commands.describe(name='The name of the counter to reset.')
    async def reset_counter(self, interaction: Interaction, name: str):
        """Resets the specified counter to 0."""
        channel_id = interaction.channel_id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await interaction.response.send_message(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] = 0
        await interaction.response.send_message(f"Counter '{name}' has been reset to 0.")

    @app_commands.command(name='showcounter', description='Shows the current value of the specified counter.')
    @app_commands.describe(name='The name of the counter to show.')
    async def show_counter(self, interaction: Interaction, name: str):
        """Shows the current value of the specified counter."""
        channel_id = interaction.channel_id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await interaction.response.send_message(f"No counter named '{name}' found in this channel.")
            return
        current_value = self.counters[channel_id][name]
        await interaction.response.send_message(f"Counter '{name}' current value: {current_value}")



    @app_commands.command(
        name="displaycounter",
        description="Display buttons for incrementing or decrementing a counter."
    )
    @app_commands.describe(name="The name of the counter to display.")
    async def display_counter(self, interaction: Interaction, name: str):
        channel_id = interaction.channel_id

        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await interaction.response.send_message(
                f"No counter named '{name}' found in this channel.",
                ephemeral=True
            )
            return
        
        view = CounterButtonView(self.counters, channel_id, name)

        await interaction.response.send_message(
            content=f"📊 **Counter `{name}`**\nCurrent value: **{self.counters[channel_id][name]}**",
            view=view
        )



    # Debug tool
    @app_commands.command(name='clearcounters', description='Clears all counters in the current channel.')
    async def clear_counters(self, interaction: Interaction):
        """Clears all counters in the current channel."""
        channel_id = interaction.channel_id
        if channel_id in self.counters:
            self.counters[channel_id] = {}
            await interaction.response.send_message("All counters in this channel have been cleared.")
        else:
            await interaction.response.send_message("No counters found in this channel to clear.")
       

async def setup(bot):
    await bot.add_cog(Counter(bot))   