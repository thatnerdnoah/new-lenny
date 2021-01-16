from typing import Text
from discord import TextChannel, Embed, Colour
from discord.ext import commands

import config
# import re, json, os

class Logger(commands.Cog, name="Logger"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.log_room: TextChannel = None
        self.mod_room: TextChannel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.mod_room = self.bot.get_channel(config.mod_channel)
        self.log_room = self.bot.get_channel(config.log_channel)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            before_id = before.author.id
            before_content = before.content
            after_content = after.content

            user = self.bot.get_user(before_id)

            if before_id == self.bot.user.id or (before_content == after_content):
                return
        
            before_embed = Embed(
                title="Before Message",
                description=f"{before_content}",
                colour=Colour.purple()
            )

            after_embed = Embed(
                title="After Message",
                description=f"{after_content}",
                colour=Colour.purple()
            )

            await self.log_room.send(f"**A message was edited by {user.name}#{user.discriminator} in #{before.channel.name}!**")
            await self.log_room.send(embed=before_embed)
            await self.log_room.send(embed=after_embed)
        except AttributeError as err:
            print(f"{err}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author.id == self.bot.user.id:
                return

            user = self.bot.get_user(message.author.id)
            embed: Embed = Embed(
                title = f"A message was deleted in #{message.channel.name}!",
                colour = Colour.purple()
            )
            embed.add_field(name="Message by", value=f"{user.name}#{user.discriminator} <{message.author.id}>", inline=False)
            embed.add_field(name="Message", value=f"{message.content}", inline=False)

            await self.log_room.send(embed=embed)
        except AttributeError as err:
            print(f"{err}")

def setup(client):
    client.add_cog(Logger(client))