"""Identical to the counting cog, but it does the alphabet in order instead of numbers."""
import string, asyncio
from discord.ext import commands
from discord import app_commands, Interaction, TextChannel, Colour
from helpers import database

try:
    import config_local as config
    local_test=True
except ImportError:
    import config

letters = list(string.ascii_lowercase)

class Alphabet(commands.Cog, name="Alphabet"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = None
        self.counting_channel: TextChannel = None
        self.log_channel: TextChannel = None
        self.last_messengar = None
        self.expected_letter = 'a'
        self.lives = 2

    async def cog_load(self):
        self.initialize()
    
    async def cog_unload(self):
        self.bot.remove_listener(self.on_message)

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize()

    def initialize(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)

        print("Before database pull:", self.expected_letter, self.lives)

        db_letter, lives = database.letter_pull()

        self.expected_letter = db_letter
        self.lives = lives

        print("After database pull:", self.expected_letter, self.lives)

        print("I am ready to cou... I mean, spell the alphabet!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                try:
                    if len(message.content) == 1:
                        message_letter = message.content
                        if not local_test:
                            if message.author == self.last_messengar:
                                await asyncio.sleep(0.1)
                                await message.add_reaction("❌")
                                await message.channel.send(f"You cannot go twice in a row, <@{message.author.id}>!")
                                await message.channel.send(f"The alphabet may continue at {self.expected_letter}!")
                
                        raise NotImplementedError("Implementation needed")
                
                
                
                
                except Exception as e:
                    return

async def setup(client):
    await client.add_cog(Alphabet(client))

