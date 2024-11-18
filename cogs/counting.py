from discord import TextChannel, File, Embed, Colour, app_commands, Interaction
from discord.ext import commands
from helpers import database
from media import meme
import random as rand

local_test = False

try:
    import config_local as config
    local_test = True
except ImportError:
    import config


class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.log_channel : TextChannel = None
        self.collect : bool = False
        self.last_messanger = None
        self.expected_number = 1
        self.record = 0
        self.lives = 3
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)

        print("Before database pull:", self.expected_number, self.record, self.lives)
        
        db_number, record_number, lives = database.database_pull()

        if db_number != 0:
            self.expected_number = db_number
            self.record = record_number
            self.lives = lives

        print("After database pull:", self.expected_number, self.record, self.lives)
        print("Counting begins!")

    @commands.command(name="setnumber", aliases=['set'])
    async def set_number(self, ctx, number_to_set: int):
        print("Command sent to set current number to", number_to_set)
        self.expected_number = number_to_set
        database.database_push(self.expected_number)
        await ctx.message.add_reaction('✅')

    @commands.command(name="restore")
    async def restore_number(self, ctx):
        try:
            print("Count will be restored")
            # current count variable for embed
            current_count = self.expected_number
            backup_number = database.pull_backup()
            if backup_number == 0:
                raise ValueError("The number must be greater than 0.")
            
            self.expected_number = backup_number
            embed = Embed(
                title="The counting has been restored!",
                type='rich',
                colour=Colour.purple()
            )
            embed.add_field(name="Current count before restore", value=current_count, inline=False)
            embed.add_field(name="Next number to type in", value=backup_number, inline=False)
            await self.log_channel.send(embed=embed)
            await ctx.message.add_reaction('✅')
        except ValueError as e:
            await ctx.message.add_reaction('❌')
            print(f"Error: {e}")
        except Exception as e:
            await ctx.message.add_reaction('？')
            print(f"Error: {e}")
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                try:
                    message_number = int(message.content)
                    if not local_test:
                        if message.author == self.last_messanger:
                                await message.add_reaction("❌")
                                await message.channel.send(f"You cannot go twice in a row, <@{message.author.id}>!")
                                await message.channel.send(f"Counting may continue at {self.expected_number}!")
                                return

                    if message_number == self.expected_number: 
                        self.last_messanger = message.author
                        await meme.upload_meme(message=message, number=self.expected_number)
                        
                        if self.expected_number == self.record + 1:
                            await message.channel.send("You broke the record!")
                        
                        self.expected_number += 1
                        database.database_push(self.expected_number)
                        await message.add_reaction("✅")
                    else:
                        if self.lives <= 1:
                            # Embed log
                            embed = Embed(
                                title="The counting stopped!",
                                type='rich',
                                colour=Colour.purple()
                            )
                            embed.add_field(name="Expected number", value=self.expected_number, inline=False)
                            embed.add_field(name="Number typed in", value=message_number, inline=False)
                            await self.log_channel.send(embed=embed)
                            
                            # set the record
                            if self.expected_number > self.record:
                                self.record = self.expected_number
                                database.update_record(self.record)

                            # reset the counter
                            database.database_copy(self.expected_number)
                            self.expected_number = 1
                            database.database_push(self.expected_number)
                            self.last_messanger = None
                            self.lives = 3
                            database.update_lives(self.lives)
                            await message.add_reaction("❌")
                            await message.channel.send(f"<@{message.author.id}> cant count!")
                        else:
                            self.lives -= 1
                            database.update_lives(self.lives)
                            
                            embed = Embed(
                                title="A life was used on counting!",
                                type='rich',
                                colour=Colour.purple()
                            )
                            embed.add_field(name="Expected number", value=self.expected_number, inline=False)
                            embed.add_field(name="Number typed in", value=message_number, inline=False)
                            embed.add_field(name="Number of lives left", value=self.lives, inline=False)
                            await self.log_channel.send(embed=embed)

                            await message.add_reaction("❌")
                            await message.channel.send(f"<@{message.author.id}> cant count!")
                            if self.lives == 1:
                                await message.channel.send(f"You have one life left! Don't waste it!")
                            else:
                                await message.channel.send(f"You have {self.lives} lives left!")

                except Exception:
                    return   
        else: 
            return
            
async def setup(client):
    await client.add_cog(Counting(client))

# helper functions
async def upload_meme(message, number):
    if number == 1:
        await message.channel.send(file=File("./media/1.jpg"))
    elif number == 10:
        ben_tits = rand.randint(0,1)
        if ben_tits == 0:
            await message.channel.send("woah 10 bits!")
        elif ben_tits == 1:
            await message.channel.send("woah ben tits!")
        else:
            await message.channel.send("woah 10 bits!")
    elif number == 21:
        await message.channel.send(file=File("./media/21.gif"))
    elif number == 25:
        await message.channel.send(file=File("./media/25.gif"))
    elif number == 42:
        await message.channel.send("the meaning of life")
    elif number == 51:
        aliens = rand.randint(0,1)
        if aliens == 0:
            await message.channel.send(file=File("./media/51.gif"))
        elif aliens == 1:
            await message.channel.send(file=File("./media/51.jpg"))
        else:
            await message.channel.send("woah 10 bits!")
    elif number == 66:
        await message.channel.send(file=File("./media/66.gif"))
    elif number == 69:
        await message.channel.send("nice", file=File("./media/69.png"))
    # elif self.expected_number == 96:
    #     await message.channel.send("not nice")
    elif number == 100:
        await message.channel.send(file=File("./media/100.gif"))
    elif number == 111:
        await message.channel.send(file=File("./media/111.gif"))
    # elif self.expected_number == 137:
    #     await message.channel.send("MAX LAFF POI... wait")
    elif number == 140:
        await message.channel.send("MAX LAFF POINTS!")
    elif number == 222:
        await message.channel.send(file=File("./media/222.gif"))
    elif number == 305:
        await message.channel.send("Dale???? Idk who dale is")
    elif number == 314:
        await message.channel.send(file=File("./media/314.gif"))
    elif number == 321:
        await message.channel.send(file=File("./media/321.gif"))
    elif number == 333:
        await message.channel.send(file=File("./media/333.gif"))
    elif number == 404:
        await message.channel.send("Error: not found", file=File("./media/404.gif"))
    elif number == 420:
        await message.channel.send("BLAZE IT!", file=File("./media/420.gif"))
    elif number == 444:
        await message.channel.send(file=File("./media/444.gif"))


    