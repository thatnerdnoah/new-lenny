import asyncio
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
        synced = await bot.tree.sync()
        for sync in synced:
            print(f"{sync}")
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        bot.get_channel(config.log_channel).send("The bot didn't load correctly. Check the server!")
        print(e)

@bot.tree.command(name="sync", description="Sync all slash commands")
async def sync(interaction: Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
    synced = await bot.tree.sync()
    for sync in synced:
        print(f"{sync}")
    print(f"Synced {len(synced)} command(s).")
    await interaction.response.send_message(f"Synced {len(synced)} command(s)!")

# @bot.tree.command(name="load_cog")
# async def load_cog_command(interaction: Interaction, cog: str, silent: bool = False) -> None:
#     if not interaction.user.guild_permissions.administrator:
#         return await interaction.response.send_message("How did you find this command?", ephemeral=True)
#     try:
#         success_text = f"The cog {cog} loaded successfully!"
#         await bot.load_extension(cog, package=f".{cog}")
#         await interaction.response.send_message(success_text, ephemeral=True) if not silent else print(success_text)
#     except Exception as e:
#         print(e)

# @bot.tree.command(name="unload_cog")
# async def unload_cog_command(interaction: Interaction, cog: str, silent: bool = False):
#     if not interaction.user.guild_permissions.administrator:
#         return await interaction.response.send_message("How did you find this command?", ephemeral=True)
#     try:
#         success_text: str = f"The cog {cog} was unloaded successfully!"
#         await bot.unload_extension(cog, package=f".{cog}")
#         await interaction.response.send_message(success_text, ephemeral=True) if not silent else print(success_text)
#     except Exception as e:
#         print(e)

# @bot.tree.command(name="reload_cog")
# async def reload_cog_command(interaction: Interaction, cog: str, silent: bool = False):
#     if not interaction.user.guild_permissions.administrator:
#         return await interaction.response.send_message("How did you find this command?", ephemeral=True)
#     try:
#         success_text: str = f"The cog {cog} was reloaded successfully!"
#         await bot.unload_extension(cog, package=f".{cog}")
#         await bot.load_extension(cog, package=f".{cog}")
#         await interaction.response.send_message(success_text, ephemeral=True) if not silent else print(success_text)
#     except Exception as e:
#         print(e)

async def main():
    async with bot:
        await bot.load_extension("cogs.cog_manager")
        await bot.start(config.token)

if __name__ == "__main__":
    asyncio.run(main())