import os
import asyncio
import logging
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from flask import Flask
from threading import Thread

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is Running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- THE BOT ---
async def start_bot():
    # Force Pyrogram to see the plugins folder
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    
    # DEBUG: Show us what files are in the plugins folder
    if os.path.exists(plugins_dir):
        files = os.listdir(plugins_dir)
        logger.info(f"Found plugins folder. Files inside: {files}")
    else:
        logger.error("plugins folder NOT FOUND in current directory!")

    bot = Client(
        name="FlixoraIDBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins") 
    )

    try:
        await bot.start()
        me = await bot.get_me()
        logger.info(f"DONE! Bot started as @{me.username}")

        # Send Startup Message
        if LOG_CHANNEL:
            try:
                await bot.send_message(LOG_CHANNEL, "✅ **Bot is Online! Commands are now working.**")
            except Exception as e:
                logger.error(f"LOG_CHANNEL ERROR: {e}")

        await idle()
        
    except Exception as e:
        logger.error(f"Bot failed: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
