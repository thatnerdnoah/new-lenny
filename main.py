import asyncio
import signal
import sys
from discord import Game, Intents, app_commands, Interaction
from discord.ext.commands import Bot

try:
    import config_local as config
except ImportError:
    import config

intents = Intents.default()
intents.message_content = True
    
bot = Bot(command_prefix='$', intents=intents, application_id=config.bot_id)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")
    try:
        await bot.change_presence(activity=Game(name="Escaping Meteor Simulator"))
    except Exception as e:
        bot.get_channel(config.log_channel).send("The bot didn't load correctly. Check the server!")
        print(e)

@bot.command(name="sync")
async def sync(ctx):
    # if not interaction.user.guild_permissions.administrator:
    #     return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
    synced = await bot.tree.sync()
    for sync in synced:
        print(f"{sync}")
    print(f"Synced {len(synced)} command(s).")
    # await interaction.response.send_message(f"Synced {len(synced)} command(s)!")
    await ctx.message.add_reaction('✅')

# async def shutdown()
#     print(f"Shutting down {bot.user.name}...")
#     await bot.close()
#     await asyncio.sleep(1)
#     sys.exit(0)

# def handle_signals():
#     loop = asyncio.get_event_loop()

#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, lambda: asyncio.ensure_future(shutdown()))

async def main():
    async with bot:
        await bot.load_extension("cogs.cog_manager")
        await bot.start(config.token)

if __name__ == "__main__":
    # handle_signals()
    
    asyncio.run(main())