import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
import traceback

class FlixoraBot(Client):
    def __init__(self):
        super().__init__(
            name="FlixoraIDBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"), # Automatically loads all files in plugins/
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"[{me.first_name}] is now Online!")
        
        # Log to Channel
        try:
            if LOG_CHANNEL:
                await self.send_message(LOG_CHANNEL, f"✅ **Bot Started!**\n\n**Name:** {me.first_name}\n**ID:** `{me.id}`")
        except Exception as e:
            print(f"Failed to send start log: {e}")

    async def stop(self, *args):
        # Log offline status before shutting down
        try:
            if LOG_CHANNEL:
                await self.send_message(LOG_CHANNEL, "⚠️ **Bot is shutting down/offline.**")
        except:
            pass
        await super().stop()
        print("Bot Stopped.")

if __name__ == "__main__":
    bot = FlixoraBot()
    bot.run()