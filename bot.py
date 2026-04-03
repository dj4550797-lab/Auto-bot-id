import os
import asyncio
import logging
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from threading import Thread
from flask import Flask

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FlixoraBot")

# --- WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT CLASS ---
class FlixoraBot(Client):
    def __init__(self):
        super().__init__(
            name="FlixoraIDBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=100
        )

    async def start(self):
        logger.info("Connecting to Telegram...")
        await super().start()
        me = await self.get_me()
        logger.info(f"DONE! Bot started as @{me.username}")
        
        if LOG_CHANNEL:
            try:
                await self.send_message(LOG_CHANNEL, "✅ **Bot is now Online!**")
                logger.info("Sent startup message to Log Channel.")
            except Exception as e:
                logger.error(f"Failed to send to Log Channel: {e}")

    async def stop(self, *args):
        logger.info("Stopping Bot...")
        await super().stop()

# --- MAIN RUNNER ---
if __name__ == "__main__":
    # Start Web Server
    logger.info("Starting Flask Web Server...")
    Thread(target=run_flask, daemon=True).start()
    
    # Run Bot
    logger.info("Initializing Bot...")
    bot = FlixoraBot()
    
    try:
        bot.run()
    except Exception as e:
        logger.critical(f"BOT CRASHED: {e}")