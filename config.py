from os import environ

token = environ["DISCORD_TOKEN"]
# admin_role = environ["MOD_ROLE"]
mod_channel = int(environ["MOD_CHANNEL"])
log_channel = int(environ["LOG_CHANNEL"])
counting_channel = int(environ["COUNTING_CHANNEL"])
cogs = ["cogs.counting"]
bot_id = 597109548104548390
prefix = "$"
project_id = environ["PROJECT_ID"]
discord_name = "Snoop Troop"

# url = 'https://api.fortnitetracker.com/v1/store'
# headers = {'TRN-Api-Key': f'{environ["FORTNITE_KEY"]}'}