from discord import TextChannel, Embed
from discord.ext import commands, tasks
from discord.ext.commands import bot

import config

class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.counter = 0
        self.expected_number = 1

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        print("Counting begins!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author == self.bot.user:
                return
            else:
                try:
                    message_number = int(message.content)
                    if message_number == self.expected_number:
                        self.counter += 1
                        self.expected_number += 1
                        await message.add_reaction("✅")
                    else:
                        self.counter = 0
                        self.expected_number = 1
                        await message.add_reaction("❌")
                        await message.channel.send(f"<@{message.author.id}> cant count! :megasRage:")
                except Exception as error:
                    print(error)   
        else: 
            return
            



def setup(client):
    client.add_cog(Counting(client))