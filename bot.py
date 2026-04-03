import os
import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from threading import Thread
from flask import Flask

# --- TINY WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Live and Running!"

def run_flask():
    # Render uses port 10000 by default
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
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"[{me.first_name}] is now Online!")
        if LOG_CHANNEL:
            try: await self.send_message(LOG_CHANNEL, f"✅ **Bot Started!**")
            except: pass

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Start the Web Server in the background (Thread)
    # This stops the "No ports detected" error on Render
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. Run the Telegram Bot
    bot = FlixoraBot()
    bot.run()