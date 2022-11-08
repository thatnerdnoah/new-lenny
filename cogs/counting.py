from threading import local
from discord import TextChannel, File, Embed, Colour, app_commands, Interaction
from discord.ext import commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

local_test = False

try:
    import config_local as config
    local_test = True
except ImportError:
    import config

import random as rand

cred = credentials.Certificate("./helpers/lennydb-94aae-firebase-adminsdk-lp085-af49ec526d.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.log_channel : TextChannel = None
        self.collect : bool = False
        self.last_messanger = None
        self.expected_number = 1
        self.record = 0
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)

        print("Before database pull:", self.expected_number, self.record)
        
        db_number, record_number = database_pull()

        if db_number != 0:
            self.expected_number = db_number
            self.record = record_number

        print("After database pull:", self.expected_number, self.record)
        print("Counting begins!")

    @commands.has_role(f"{config.admin_role}")
    @commands.command(name="setnumber", aliases=['set'])
    async def set_number(self, ctx, number_to_set: int):
        print("Command sent to set current number to", number_to_set)
        self.expected_number = number_to_set
        database_push(self.expected_number)
        await ctx.message.add_reaction('✅')

    @app_commands.command(name="setcount", description="Sets the count of the counting channel.")
    async def set_number(self, interaction:Interaction, number_to_set: int):
        user_permissions = interaction.user.guild_permissions
        if user_permissions.manage_channels:
            print("Command sent to set current number to", number_to_set)
            self.expected_number = number_to_set
            database_push(self.expected_number)
            await interaction.response.send_message(f"Counting has been set to {number_to_set}", ephermeral=True)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                try:
                    message_number = int(message.content)

                    if message.author == self.last_messanger and not local_test:
                            await message.add_reaction("❌")
                            await message.channel.send(f"You cannot go twice in a row, <@{message.author.id}>!")
                            await message.channel.send("Counting may continue!")
                            return

                    if message_number == self.expected_number: 
                        self.last_messanger = message.author
                        if self.expected_number == 1:
                            await message.channel.send(file=File("./media/1.jpg"))
                        elif self.expected_number == 10:
                            ben_tits = rand.randint(0,1)
                            if ben_tits == 0:
                                await message.channel.send("woah 10 bits!")
                            elif ben_tits == 1:
                                await message.channel.send("woah ben tits!")
                            else:
                                await message.channel.send("woah 10 bits!")
                        elif self.expected_number == 21:
                            await message.channel.send(file=File("./media/21.gif"))
                        elif self.expected_number == 25:
                            await message.channel.send(file=File("./media/25.gif"))
                        elif self.expected_number == 42:
                            await message.channel.send("the meaning of life")
                        elif self.expected_number == 51:
                            aliens = rand.randint(0,1)
                            if aliens == 0:
                                await message.channel.send(file=File("./media/51.gif"))
                            elif aliens == 1:
                                await message.channel.send(file=File("./media/51.jpg"))
                            else:
                                await message.channel.send("woah 10 bits!")
                        elif self.expected_number == 69:
                            await message.channel.send("nice", file=File("./media/69.png"))
                        elif self.expected_number == 96:
                            await message.channel.send("not nice")
                        elif self.expected_number == 100:
                            await message.channel.send(file=File("./media/100.gif"))
                        elif self.expected_number == 111:
                            await message.channel.send(file=File("./media/111.gif"))
                        elif self.expected_number == 137:
                            await message.channel.send("MAX LAFF POI... wait")
                        elif self.expected_number == 140:
                            await message.channel.send("MAX LAFF POINTS!")
                        elif self.expected_number == 222:
                            await message.channel.send(file=File("./media/222.gif"))
                        elif self.expected_number == 305:
                            await message.channel.send("Dale???? Idk who dale is")
                        # elif self.expected_number == 314:
                        #     await message.channel.send(file=File("./media/314.gif"))
                        elif self.expected_number == 321:
                            await message.channel.send(file=File("./media/321.gif"))
                        elif self.expected_number == 333:
                            await message.channel.send(file=File("./media/333.gif"))
                        elif self.expected_number == 404:
                            await message.channel.send("Error: not found", file=File("./media/404.gif"))
                        elif self.expected_number == 420:
                            await message.channel.send("BLAZE IT!", file=File("./media/420.gif"))
                        if self.expected_number == self.record + 1:
                            await message.channel.send("You broke the record!")
                        
                        self.expected_number += 1
                        database_push(self.expected_number)
                        await message.add_reaction("✅")
                    else:
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
                            update_record(self.record)

                        # reset the counter
                        self.expected_number = 1
                        database_push(self.expected_number)
                        self.last_messanger = None
                        await message.add_reaction("❌")
                        await message.channel.send(f"<@{message.author.id}> cant count!")

                except Exception:
                    return   
        else: 
            return
            
async def setup(client):
    await client.add_cog(Counting(client))
    # await client.tree.sync()

def database_pull():
    expected_number : int = 0
    record : int = 0

    if not config.local_test:
        doc_ref = db.collection(u'counting').document(u'count')
    else:
        doc_ref = db.collection(u'counting').document(u'count_test')
        

    doc = doc_ref.get()
    if doc.exists:
        expected_number = doc.to_dict()['count']
        record = doc.to_dict()['reward']

    return expected_number, record

def update_record(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')

    counter_ref.update({
        u'reward': num
    })

def database_push(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')

    counter_ref.update({
        u'count': num
    })