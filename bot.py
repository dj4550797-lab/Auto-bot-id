import os
import asyncio
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from flask import Flask
from threading import Thread

# --- COOL ASCII ART & ABOUT SECTION ---
ASCII_ART = """
███████╗██╗     ██╗██╗  ██╗ ██████╗ ██████╗  █████╗ 
██╔════╝██║     ██║╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗
█████╗  ██║     ██║ ╚███╔╝ ██║   ██║██████╔╝███████║
██╔══╝  ██║     ██║ ██╔██╗ ██║   ██║██╔══██╗██╔══██║
██║     ███████╗██║██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║
╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
         🌟 ADVANCED GROUP & ID BOT 🌟
"""

# --- WEB SERVER FOR RENDER/HEROKU ---
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Flixora ID Bot is Running Beautifully! 🚀</h1>"

def run_web():
    # Render and Heroku use the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- THE BOT CLIENT ---
class FlixoraBot(Client):
    def __init__(self):
        super().__init__(
            name="FlixoraIDBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            ipv6=False # <--- FIX FOR RENDER 40-MINUTE DELAY
        )

async def start_bot():
    bot = FlixoraBot()
    
    print(ASCII_ART)
    print("🔄 Starting Bot...")
    
    try:
        await bot.start()
        me = await bot.get_me()
        print(f"🚀 Bot successfully started as @{me.username}")
        print("✅ Web Server & Bot are running simultaneously.")
        
        # Send Startup Message to Log Channel
        if LOG_CHANNEL != 0:
            try:
                await bot.send_message(
                    LOG_CHANNEL,
                    f"**🚀 Bot Started Successfully!**\n\n"
                    f"**🤖 Bot Name:** {me.first_name}\n"
                    f"**🔗 Username:** @{me.username}\n"
                    f"**⚙️ Status:** Online & Ready!"
                )
            except Exception as e:
                print(f"⚠️ Could not send message to Log Channel: {e}")
                
        await idle()
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    # Start web server in a separate background thread
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    # Run the bot
    asyncio.run(start_bot())
