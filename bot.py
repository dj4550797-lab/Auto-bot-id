import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand
from aiohttp import web

# --- Fetch credentials ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = os.environ.get("PORT", "8080") # Render provides this automatically

app = Client("FlixoraIDBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- SIMPLE WEB SERVER FOR RENDER ---
async def handle(request):
    return web.Response(text="Flixora ID Bot is Alive!")

async def start_web_server():
    server = web.Application()
    server.add_routes([web.get('/', handle)])
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    print(f"Web server started on port {PORT}")

# --- BOT COMMANDS ---
@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message):
    await message.reply_text(f"👋 **Hello {message.from_user.first_name}!**\n\nI am Flixora ID Bot. Send /id to get started!", quote=True)

@app.on_message(filters.command("id"))
async def id_command(client, message):
    text = f"**📌 Chat ID:** `{message.chat.id}`\n"
    if message.from_user:
        text += f"**👤 Your ID:** `{message.from_user.id}`\n"
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"**🎯 Replied User ID:** `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"**📢 Forwarded Channel ID:** `{message.reply_to_message.forward_from_chat.id}`\n"
    await message.reply_text(text, quote=True)

@app.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id_command(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        await message.reply_text(f"**🎟 Sticker File ID:**\n`{message.reply_to_message.sticker.file_id}`", quote=True)
    else:
        await message.reply_text("⚠️ Please reply to a sticker!", quote=True)

# --- MAIN RUNNER ---
async def main():
    print("Starting Web Server...")
    await start_web_server()
    
    print("Starting Bot...")
    await app.start()
    
    await app.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("id", "Get ID details"),
        BotCommand("stickerid", "Get Sticker ID")
    ])
    
    print("Bot is fully active!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
