from os import environ

token = environ["DISCORD_TOKEN"]
mod_channel = int(environ["MOD_CHANNEL"])
log_channel = int(environ["LOG_CHANNEL"])
cogs = ["cogs.item_shop", "cogs.logger"]
prefix = "$"
shop_channel = int(environ["FORTNITE_CHANNEL"])


fortnite_store_url = 'https://api.fortnitetracker.com/v1/store'
fortnite_header = {'TRN-Api-Key': f'{environ["FORTNITE_KEY"]}'}