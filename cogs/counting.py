from discord import TextChannel, File, Embed, Colour
from discord.ext import commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import config

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
        self.expected_number = number_to_set
        database_push(self.expected_number)
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                if message.author == self.last_messanger:
                    return
                try:
                    message_number = int(message.content)
                    if message_number == self.expected_number:
                        self.last_messanger = message.author

                        if self.expected_number == 10:
                            await message.channel.send("woah 10 bits!")
                        elif self.expected_number == 24:
                            await message.channel.send(file=File("./media/24.gif"))
                        elif self.expected_number == 25:
                            await message.channel.send(file=File("./media/25.gif"))
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
                        elif self.expected_number == 321:
                            await message.channel.send(file=File("./media/321.gif"))
                        elif self.expected_number == 420:
                            await message.channel.send("Blaze it!")
                        elif self.expected_number == self.record + 1:
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
            
def setup(client):
    client.add_cog(Counting(client))

def database_pull():
    expected_number : int = 0
    record : int = 0

    doc_ref = db.collection(u'counting').document(u'count')

    doc = doc_ref.get()
    if doc.exists:
        expected_number = doc.to_dict()['count']
        record = doc.to_dict()['reward']

    return expected_number, record

def update_record(num: int):
    counter_ref = db.collection(u'counting').document(u'count')
    counter_ref.update({
        u'reward': num
    })

def database_push(num: int):
    counter_ref = db.collection(u'counting').document(u'count')
    counter_ref.update({
        u'count': num
    })