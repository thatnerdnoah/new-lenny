from discord import Embed, Colour, app_commands, Interaction
from discord.ext import commands
import re   

# Standard twitter and instagram links in regular expressions
TWITTER_LINK_PATTERN = r'https?://(?:www\.)?(?:twitter\.com|x\.com)/[^\s]+'
INSTAGRAM_LINK_PATTERN = r'https?://(?:www\.)?instagram\.com/[^\s]+'


class Link(commands.Cog, name="Link"):
    """
    This cog is designed to correct Twitter and Instagram links. x.com or twitter.com would convert to fxtwitter.com. instagram.com will go to oginstagram.com
    """

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize_cog()

    async def cog_load(self) -> None:
        self.initialize_cog()

    def initialize_cog(self):
        print("Link corrector loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        #  Find Twitter and Instagram links in the message content
        twitter_links = re.findall(TWITTER_LINK_PATTERN, message.content)
        instagram_links = re.findall(INSTAGRAM_LINK_PATTERN, message.content)

        if message.embeds and (twitter_links or instagram_links):
            await message.edit(suppress=True)

        # Correct Twitter links
        for link in twitter_links:
            corrected_link = link.replace("twitter.com", "fxtwitter.com").replace("x.com", "fxtwitter.com")
            await message.reply(f"Fixing link: {corrected_link}", mention_author=False)

        # Correct Instagram links
        for link in instagram_links:
            corrected_link = link.replace("instagram.com", "oginstagram.com")
            await message.reply(f"Fixing link: {corrected_link}", mention_author=False)


async def setup(bot):
    await bot.add_cog(Link(bot))