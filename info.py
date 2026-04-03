import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Log Channel & Admins
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0)) # Example: -100123456789
ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split(",") if x.strip()] # Example: 123456,789012

# MongoDB Database URI
MONGO_URI = os.environ.get("MONGO_URI", "") # Get this from MongoDB Atlas
DB_NAME = os.environ.get("DB_NAME", "FlixoraBotDB")