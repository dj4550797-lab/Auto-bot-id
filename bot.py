import os
import asyncio
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Flixora ID Bot is Running!</h1>"

def run_web():
    # Render uses environment variable PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- THE BOT ---
async def start_bot():
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
        print(f"🚀 Bot started as @{me.username}")
        await idle()
    except Exception as e:
        print(f"❌ Bot failed: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    # Start web server in a separate thread
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    # Run the bot
    asyncio.run(start_bot())
