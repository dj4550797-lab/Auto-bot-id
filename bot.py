from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FlixoraID",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("🚀 Flixora ID Bot is Online!")
        await idle()

if __name__ == "__main__":
    Bot().run()
