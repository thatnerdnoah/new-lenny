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

class Alphabet(commands.Cog, name="Alphabet"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel: TextChannel = None
        self.log_channel: TextChannel = None
        self.letters = list(string.ascii_lowercase)
        self.last_messanger = None
        self.expected_letter = 'a'
        self.current_index = 0
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
        self.current_index = self.letters.index(self.expected_letter)

        print("After database pull:", self.expected_letter, self.lives)

        print("I am ready to cou... I mean, spell the alphabet!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                try:
                    if len(message.content) == 1:  # Ensure it's a single character
                        message_letter = message.content.lower()

                        if message.author == self.last_messanger and not local_test:
                            await message.add_reaction("❌")
                            await message.channel.send(
                                f"You cannot go twice in a row, <@{message.author.id}>!"
                            )
                            await message.channel.send(
                                f"The alphabet may continue at {self.letters[self.current_index]}!"
                            )
                            return

                        if message_letter == self.letters[self.current_index]:
                            self.current_index += 1
                            # database.letter_push(self.letters[self.current_index])
                            self.last_messanger = message.author
                            await message.add_reaction("✅")

                            # Reset if we've reached the end of the alphabet
                            if self.current_index >= len(self.letters):
                                await message.channel.send("Congratulations! You've completed the alphabet!")
                                await self.reset_game()
                        else:
                            self.lives -= 1
                            await message.add_reaction("❌")
                            await message.channel.send(
                                f"Wrong letter, <@{message.author.id}>! The alphabet may continue at {self.letters[self.current_index]}. "
                                f"Lives remaining: {self.lives}"
                            )
                            if self.lives <= 0:
                                await self.reset_game()
                except Exception:
                    return
                
    async def reset_game(self):
        """Reset the game when lives run out or alphabet is completed."""
        self.current_index = 0
        self.expected_letter = 'a'
        if self.lives <= 0:
            self.lives = 2
        await self.counting_channel.send("Game over! Restarting at 'a'.")

async def setup(client):
    await client.add_cog(Alphabet(client))

