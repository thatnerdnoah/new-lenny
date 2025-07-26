from dotenv import load_dotenv
import os

load_dotenv()

token = str(os.getenv("DISCORD_TOKEN"))
mod_channel = int(os.getenv("MOD_CHANNEL"))
log_channel = int(os.getenv("LOG_CHANNEL"))
counting_channel = int(os.getenv("COUNTING_CHANNEL"))
cogs = ["cogs.counting", "cogs.dice"]
bot_id = int(os.getenv("BOT_ID"))
project_id = str(os.getenv("PROJECT_ID"))
discord_name = str(os.getenv("DISCORD_NAME"))
path_to_credential = str(os.getenv("CRED_FILE"))
local_test = False
