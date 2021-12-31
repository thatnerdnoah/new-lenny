from discord import TextChannel, Embed, Colour
from discord.ext import commands, tasks

import config

import re
import json
import os

class Warning(commands.Cog, name="Moderation"):
    """Moderation cog for Discord Bots."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.mod_room: TextChannel = None
        self.log_room: TextChannel = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.mod_room = self.bot.get_channel(config.mod_channel)
        self.log_room = self.bot.get_channel(config.log_channel)
        print("Warning live!")

    @commands.command(name="warn", aliases=['w'])
    async def warning(self, ctx, user_id: int):
        """Warns the user of their actions and grants the user strikes. The reason must be in quotation marks."""
        channel = ctx.channel

        await ctx.channel.send("Please state the reason for the warning in your next message.")

        def check(m):
            return m.channel == channel

        reason: str = await self.bot.wait_for("message", check=check)
        
        user = self.bot.get_user(user_id)
        await user.send(
            f"The moderators of {config.discord_name} have given you a warning for the following reason: \n\n{reason}\n\nPlease review the rules and be careful not to obtain more strikes. If you have any questions, message one of the moderators."
        )
        await print("Message sent")
        await ctx.message.add_reaction('✅')
        

def setup(client):
    client.add_cog(Warning(client))