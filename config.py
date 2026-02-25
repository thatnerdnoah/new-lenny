from dotenv import load_dotenv
import os

load_dotenv()

def get_env(name: str, *, required: bool = False, default=None) -> str:
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_int_env(name: str, *, required: bool = False, default=None) -> int:
    value = os.getenv(name, default)
    if value is None:
        if required:
            raise ValueError(f"Missing required environment variable: {name}")
        return None

    # Strip accidental quotes (Docker .env gotcha)
    value = value.strip().strip('"').strip("'")

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{name} must be an integer (got: {value})")


# 🔑 Required
token = get_env("DISCORD_TOKEN", required=True)

# 🔢 Discord IDs
mod_channel = get_int_env("MOD_CHANNEL", required=True)
log_channel = get_int_env("LOG_CHANNEL", required=True)
counting_channel = get_int_env("COUNTING_CHANNEL", required=True)
bot_id = get_int_env("BOT_ID", required=True)

# 🧾 Optional / metadata
project_id = get_env("PROJECT_ID")
discord_name = get_env("DISCORD_NAME")
path_to_credential = get_env("CRED_FILE")

# ⚙️ Bot configuration
cogs = os.getenv("COGS", "").split(",")

# 🧪 Environment flag
local_test = get_env("LOCAL_TEST", default="false").lower() == "true"
