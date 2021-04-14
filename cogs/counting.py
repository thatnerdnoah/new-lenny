from discord import TextChannel, File, Embed, Colour
from discord.ext import commands

import config

class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.log_channel : TextChannel = None
        self.last_messanger = None
        self.counter = 0
        self.expected_number = 1

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)
        print("Counting begins!")

    @commands.has_role(f"{config.admin_role}")
    @commands.command(name="setnumber", aliases=['set'])
    async def set_number(self, ctx, number_to_set: int):
        if ctx.channel == self.counting_channel:
            self.expected_number = number_to_set
            self.counter = number_to_set - 1
            await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
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
                        if self.expected_number == 10:
                            await message.channel.send("woah 10 bits!")
                        elif self.expected_number == 42:
                            await message.channel.send("the meaning of life")
                        elif self.expected_number == 69:
                            await message.channel.send("nice", file=File("./media/69.png"))
                        elif self.expected_number == 96:
                            await message.channel.send("not nice")
                        elif self.expected_number == 100:
                            await message.channel.send(file=File("./media/100.gif"))
                        elif self.expected_number == 137:
                            await message.channel.send("MAX LAFF POINTS!")
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
                        embed = Embed(
                            title="The counting stopped!",
                            type='rich',
                            colour=Colour.purple()
                        )
                        embed.add_field(name="Expected number", value=self.expected_number, inline=True)
                        embed.add_field(name="Number typed in", value=message_number, inline=True)
                        embed.add_field(name="Counter number", value=self.counter, inline=True)

                        await self.log_channel.send(embed=embed)
                except Exception:
                    return   
        else: 
            return
            
def setup(client):
    client.add_cog(Counting(client))