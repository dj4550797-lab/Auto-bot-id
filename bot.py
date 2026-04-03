import os
import asyncio
import logging
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from flask import Flask
from threading import Thread

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def index():
    return "<h1>Flixora Bot is Running!</h1>"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- THE BOT ---
async def start_bot():
    # Get the absolute path to the plugins folder
    plugins_path = os.path.join(os.path.dirname(__file__), "plugins")
    
    logger.info(f"Checking for plugins in: {plugins_path}")
    if not os.path.exists(plugins_path):
        logger.error("CRITICAL: 'plugins' folder not found!")

    bot = Client(
        name="FlixoraIDBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins") # This looks in the 'plugins' folder
    )

    try:
        await bot.start()
        me = await bot.get_me()
        logger.info(f"DONE! Bot started as @{me.username}")

        if LOG_CHANNEL:
            try:
                await bot.send_message(LOG_CHANNEL, "✅ **Bot is now Online and Plugins are loaded!**")
            except Exception as e:
                logger.error(f"LOG_CHANNEL ERROR: {e}. Check if bot is ADMIN in {LOG_CHANNEL}")

        await idle()
        
    except Exception as e:
        logger.error(f"Bot failed: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())