import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = os.environ.get("PORT", "10000")

app = Client("FlixoraIDBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- WEB SERVER (For Render) ---
async def handle(request):
    return web.Response(text="Flixora ID Finder is Alive!")

async def start_web_server():
    server = web.Application()
    server.add_routes([web.get('/', handle)])
    runner = web.AppRunner(server); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(PORT)).start()

# --- START COMMAND (Stylish Format) ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    welcome_text = f"""🔷 𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗜𝗗 𝗙𝗜𝗡𝗗𝗘𝗥 🔶
━━━━━━━━━━━━━━━━━
🎉 𝗪𝗘𝗟𝗖𝗢𝗠𝗘, —‌‌ {user_name} ! 🎉
━━━━━━━━━━━━━━━━━━━ 
🟡 𝗪𝗛𝗔𝗧 𝗖𝗔𝗡 𝗜 𝗗𝗢 ❓
┠ 📢 Channel ID
┠ 👥 Group ID 
┠ 🤖 Bot ID 
┠ 👤 User ID 
┗ ⭐ Premium User ID 

━ Powered by @FlixoraUpdates 

👇 𝗡𝗘𝗖𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗣𝗥𝗘𝗦𝗦 𝗞𝗔𝗥𝗢 𝗔𝗨𝗥 𝗕𝗢𝗧 𝗣𝗔𝗔𝗢 ! 👇"""
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Flixora to Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/FlixoraUpdates"), InlineKeyboardButton("🛠 Support", url="https://t.me/FlixoraSupport")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=btns)

# --- ID COMMAND ---
@app.on_message(filters.command("id"))
async def id_finder(client, message):
    text = f"🔷 **𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗜𝗗 𝗗𝗘𝗧𝗔𝗜𝗟𝗦** 🔶\n━━━━━━━━━━━━━━━━━\n"
    text += f"📌 **Chat ID:** `{message.chat.id}`\n"
    
    if message.from_user:
        text += f"👤 **User ID:** `{message.from_user.id}`\n"
        if message.from_user.is_premium:
            text += f"⭐ **Account:** `Premium User`\n"
    
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"🎯 **Replied User:** `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"📢 **Channel ID:** `{message.reply_to_message.forward_from_chat.id}`\n"
            
    await message.reply_text(text, quote=True)

# --- STICKER ID & PREVIEW FEATURE ---
@app.on_message(filters.sticker | filters.text)
async def sticker_logic(client, message):
    # Agar user sticker bheje toh ID bataye
    if message.sticker:
        sticker_id = message.sticker.file_id
        await message.reply_text(f"🎟 **Flixora Sticker ID:**\n`{sticker_id}`", quote=True)
    
    # Agar user Sticker ID likhe toh Sticker wapas bheje (Preview)
    elif message.text and message.text.startswith("CAAC"):
        try:
            await message.reply_sticker(sticker=message.text)
            await message.reply_text("✨ **Above is the preview of your Sticker ID!**")
        except:
            pass # Agar valid ID nahi hai toh ignore kare

# --- STARTUP ---
async def main():
    await start_web_server()
    await app.start()
    await app.set_bot_commands([
        BotCommand("start", "Main Menu"),
        BotCommand("id", "Get IDs"),
        BotCommand("help", "Support")
    ])
    print("Flixora ID Bot is Running!")
    await idle()

if __name__ == "__main__":
    app.run(main())
