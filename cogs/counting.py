from discord import TextChannel, Embed
from discord.ext import commands, tasks
from discord.ext.commands import bot, cooldown

import config

class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.last_messanger = None
        self.counter = 0
        self.expected_number = 1

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        print("Counting begins!")


    @commands.has_role(f"{config.admin_role}")
    @commands.command(name="setnumber", aliases=['set'])
    async def set_number(self, ctx, number_to_set):
        if ctx.channel == self.counting_channel:
            self.expected_number = number_to_set
            self.counter = number_to_set - 1
            await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author == self.bot.user:
                return
            else:
                if message.author == self.last_messanger:
                    return
                try:
                    message_number = int(message.content)
                    if message_number == self.expected_number:
                        if self.expected_number == 69:
                            await message.channel.send("nice")
                        elif self.expected_number == 96:
                            await message.channel.send("not nice")
                        elif self.expected_number == 100:
                            await message.channel.send("you gay")
                        elif self.expected_number == 420:
                            await message.channel.send("blaze it!")
                        self.last_messanger = message.author
                        self.counter += 1
                        self.expected_number += 1
                        await message.add_reaction("✅")
                    else:
                        self.counter = 0
                        self.expected_number = 1
                        self.last_messanger = None
                        await message.add_reaction("❌")
                        await message.channel.send(f"<@{message.author.id}> cant count!")
                except Exception as error:
                    return   
        else: 
            return
            



def setup(client):
    client.add_cog(Counting(client))