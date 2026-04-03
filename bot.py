from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL

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
            try: await self.send_message(LOG_CHANNEL, f"✅ **Bot Started!**\n**ID:** `{me.id}`")
            except: pass

    async def stop(self, *args):
        if LOG_CHANNEL:
            try: await self.send_message(LOG_CHANNEL, "⚠️ **Bot is shutting down/offline.**")
            except: pass
        await super().stop()
        print("Bot Stopped.")

if __name__ == "__main__":
    FlixoraBot().run()