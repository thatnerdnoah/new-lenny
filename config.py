from os import environ

token = environ["DISCORD_TOKEN"]
mod_channel = int(environ["MOD_CHANNEL"])
log_channel = int(environ["LOG_CHANNEL"])
counting_channel = int(environ["COUNTING_CHANNEL"])
cogs = ["cogs.item_shop", "cogs.logger"]
prefix = "$"
shop_channel = int(environ["FORTNITE_CHANNEL"])


url = 'https://api.fortnitetracker.com/v1/store'
headers = {'TRN-Api-Key': f'{environ["FORTNITE_KEY"]}'}