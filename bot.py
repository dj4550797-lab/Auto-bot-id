import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- Fetch credentials ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = os.environ.get("PORT", "8080")

# --- CUSTOMIZATION ---
# You can change this Sticker ID using your own /stickerid command later!
FETCH_STICKER = "CAACAgIAAxkBAAMIacD-Ra4_z1RuU2JTyYBeqq-qHrUAAvUAA_cCyA9HRphh0VDIsR4E"

app = Client("FlixoraIDBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- WEB SERVER FOR RENDER ---
async def handle(request):
    return web.Response(text="Flixora ID Bot is running with Loading Section!")

async def start_web_server():
    server = web.Application()
    server.add_routes([web.get('/', handle)])
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()

# --- ID COMMAND WITH LOADING SECTION ---
@app.on_message(filters.command("id"))
async def id_command(client, message):
    # 1. Send Loading Section
    loading_msg = await message.reply_sticker(
        sticker=FETCH_STICKER,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⏳ Flixora is fetching IDs...", callback_data="loading")]]
        )
    )
    
    # 2. Small artificial delay for "Pro" look
    await asyncio.sleep(1.5)
    
    # 3. Prepare ID Data
    text = f"**📊 FLIXORA ID DETAILS**\n\n"
    text += f"**📌 Chat ID:** `{message.chat.id}`\n"
    if message.from_user:
        text += f"**👤 Your ID:** `{message.from_user.id}`\n"
    
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"**🎯 Replied User ID:** `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"**📢 Forwarded Channel ID:** `{message.reply_to_message.forward_from_chat.id}`\n"

    # 4. Remove loading and show final result
    await loading_msg.delete()
    await message.reply_text(text, quote=True)

# --- STICKER ID COMMAND WITH LOADING ---
@app.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id_command(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        # Loading msg
        loading = await message.reply_text("✨ Analyzing Sticker...")
        await asyncio.sleep(1)
        
        file_id = message.reply_to_message.sticker.file_id
        await loading.edit_text(f"**🎟 Sticker File ID:**\n`{file_id}`")
    else:
        await message.reply_text("⚠️ Please reply to a sticker!", quote=True)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        "I am **Flixora ID Bot**. I can fetch User, Group, and Sticker IDs with style.\n\n"
        "🚀 Click the **Menu** button to see commands!",
        quote=True
    )

# --- MAIN RUNNER ---
async def main():
    await start_web_server()
    await app.start()
    
    await app.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("id", "Fetch IDs with Loading Section"),
        BotCommand("stickerid", "Get Sticker File ID")
    ])
    
    print("Bot & Web Server Active!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
