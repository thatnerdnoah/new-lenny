import time

from discord import TextChannel, Embed
from discord.ext import commands, tasks

import config
from helpers import web_request as web
from helpers import store_handler as SH

class ItemShop(commands.Cog, name="ItemShop"):
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
        self.item_shop_channel : TextChannel = None
        self.current_store = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.item_shop_channel = self.bot.get_channel(config.shop_channel)

        store_from_file, did_complete = SH.load_store('store.csv')
        if did_complete:
            self.current_store = store_from_file

        self.handle_store.start()

    @tasks.loop(seconds=60)
    async def handle_store(self):
        cTime = time.strftime("%Y/%m/%d-%H:%M")
        print(f"Running Item Shop refresh @ {cTime}")

        code, store = await web.web_request(config.url, headers=config.headers)
        
        if code != 200:
            print(f"Code was {code}")
            return
        
        if store == [] or len(store) <= 0:
            print(f"API returned nothing: len() => {len(store)}")
            return
        
        if not self.current_store or not SH.compare_store(store, self.current_store):
            print("Saving new store...")
            self.current_store = store
            SH.save_store(store)

            print("Refreshing...")
            await self.clear_messages()

            for item in self.current_store:
                await self.post_item(item)

            del store
            print("Refresh finished!")
        else:
            print("API returned the same store")
            del store
            return

    async def post_item(self, item):
        embed = Embed(
            title=SH.correct_names(item['name']),
            type='rich',
            description="Item Shop Item",
            colour=SH.set_rarity_color(item)
        )
        embed.add_field(name='Cost', value=f"{SH.correct_price(item)} V-Bucks")
        embed.add_field(name='Rarity', value=SH.correct_rarities(item))
        if item['imageUrl'] != 'unknown':
            embed.set_thumbnail(url=item['imageUrl'])

        await self.item_shop_channel.send(embed=embed)

    async def clear_messages(self):
		# Deletes all of the messages in the fortnite channel
        async for message in self.item_shop_channel.history(limit=100):
            if message.author.id == self.bot.user.id:
                await message.delete()

def setup(client):
    client.add_cog(ItemShop(client))