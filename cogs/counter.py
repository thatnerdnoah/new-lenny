### Cog for creating and managing counters in Discord channels.

import discord
from discord.ext import commands

class Counter(commands.Cog):
    """A cog for creating and managing counters in Discord channels."""

    def __init__(self, bot):
        self.bot = bot
        self.counters = {}  # Dictionary to store counters for each channel

    @commands.command(name='createcounter')
    async def create_counter(self, ctx, name: str):
        """Creates a new counter with the given name."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters:
            self.counters[channel_id] = {}
        if name in self.counters[channel_id]:
            await ctx.send(f"A counter named '{name}' already exists in this channel.")
            return
        self.counters[channel_id][name] = 0
        await ctx.send(f"Counter '{name}' created with an initial value of 0.")

    @commands.command(name='increment')
    async def increment_counter(self, ctx, name: str):
        """Increments the specified counter by 1."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await ctx.send(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] += 1
        await ctx.send(f"Counter '{name}' incremented. Current value: {self.counters[channel_id][name]}")

    @commands.command(name='decrement')
    async def decrement_counter(self, ctx, name: str):
        """Decrements the specified counter by 1."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await ctx.send(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] -= 1
        await ctx.send(f"Counter '{name}' decremented. Current value: {self.counters[channel_id][name]}")

    @commands.command(name='resetcounter')
    async def reset_counter(self, ctx, name: str):
        """Resets the specified counter to 0."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await ctx.send(f"No counter named '{name}' found in this channel.")
            return
        self.counters[channel_id][name] = 0
        await ctx.send(f"Counter '{name}' has been reset to 0.")

    @commands.command(name='showcounter')
    async def show_counter(self, ctx, name: str):
        """Shows the current value of the specified counter."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await ctx.send(f"No counter named '{name}' found in this channel.")
            return
        await ctx.send(f"Counter '{name}' current value: {self.counters[channel_id][name]}")

    @commands.command(name='deletecounter')
    async def delete_counter(self, ctx, name: str):
        """Deletes the specified counter."""
        channel_id = ctx.channel.id
        if channel_id not in self.counters or name not in self.counters[channel_id]:
            await ctx.send(f"No counter named '{name}' found in this channel.")
            return
        del self.counters[channel_id][name]
        await ctx.send(f"Counter '{name}' has been deleted.")   

def setup(bot):
    bot.add_cog(Counter(bot))