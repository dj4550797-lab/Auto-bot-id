import os
import asyncio
import time
import psutil
import platform
from datetime import datetime
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Render Port Fix
PORT_STR = os.environ.get("PORT", "10000")
PORT = int(PORT_STR) if PORT_STR.isdigit() else 10000

app = Client("FlixoraIDBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
boot_time = time.time()

# --- WEB SERVER (For Render) ---
async def handle(request):
    return web.Response(text="Flixora Pro Ecosystem is Live!")

async def start_web_server():
    server = web.Application()
    server.add_routes([web.get('/', handle)])
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web Server started on port {PORT}")

# --- START COMMAND ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    welcome_text = f"""🔷 𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗜𝗗 𝗙𝗜𝗡𝗗𝗘𝗥 🔶
━━━━━━━━━━━━━━━━━
🎉 𝗪𝗘𝗟𝗖𝗢𝗠𝗘, —‌‌ {user_name} ! 🎉
━━━━━━━━━━━━━━━━━━━ 
🟡 𝗪𝗛𝗔𝗧 𝗖𝗔𝗡 𝗜 𝗗𝗢 ❓
┠ 📢 Channel ID -> `/id`
┠ 👥 Group ID -> `/id`
┠ 👤 User ID -> `/id`
┠ 🎟 Sticker ID -> `/stickerid`
┠ 👁 Preview -> `/getsticker`
┗ 🖥 System Info -> `/system`

━ Powered by @Amarhacker

👇 𝗡𝗘𝗖𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗣𝗥𝗘𝗦𝗦 𝗞𝗔𝗥𝗢 𝗔𝗨𝗥 𝗕𝗢𝗧 𝗣𝗔𝗔𝗢 ! 👇"""
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Flixora to Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/flixoraoffiacial"), InlineKeyboardButton("🛠 Support", url="https://t.me/FlixoraSupport")]
    ])
    await message.reply_text(welcome_text, reply_markup=btns)

# --- ID COMMAND ---
@app.on_message(filters.command("id"))
async def id_finder(client, message):
    text = f"🔷 **𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗜𝗗 𝗗𝗘𝗧𝗔𝗜𝗟𝗦** 🔶\n━━━━━━━━━━━━━━━━━\n"
    text += f"📌 **Chat ID:** `{message.chat.id}`\n"
    
    if message.from_user:
        text += f"👤 **Your ID:** `{message.from_user.id}`\n"
        text += f"🌟 **Premium:** `{'✅ Yes' if message.from_user.is_premium else '❌ No'}`\n"
    
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.from_user:
            text += f"🎯 **Replied User ID:** `{reply.from_user.id}`\n"
            text += f"⭐ **Replied Premium:** `{'✅ Yes' if reply.from_user.is_premium else '❌ No'}`\n"
        
        # Unique ID Extractors
        if reply.sticker:
            text += f"🆔 **Sticker Unique ID:** `{reply.sticker.file_unique_id}`\n"
        elif reply.document:
            text += f"🆔 **File Unique ID:** `{reply.document.file_unique_id}`\n"
            
    await message.reply_text(text, quote=True)

# --- GET STICKER COMMAND (ID to Sticker) ---
@app.on_message(filters.command("getsticker"))
async def get_sticker_preview(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/getsticker [Sticker_File_ID]`")
    
    sticker_id = message.command[1]
    try:
        await message.reply_sticker(sticker=sticker_id)
        await message.reply_text("✨ **Above is your Sticker Preview!**")
    except Exception as e:
        await message.reply_text(f"❌ **Invalid ID or Error:** `{e}`")

# --- STICKER ID COMMAND (Sticker to ID) ---
@app.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id_getter(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker = message.reply_to_message.sticker
        text = f"""🎟 **𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 𝗜𝗗**
━━━━━━━━━━━━━━━━━
📂 **File ID:** 
`{sticker.file_id}`

🆔 **Unique ID:** 
`{sticker.file_unique_id}`"""
        await message.reply_text(text, quote=True)
    else:
        await message.reply_text("⚠️ **Hero, kisi sticker ko reply karke `/stickerid` likho!**", quote=True)

# --- SYSTEM COMMAND ---
@app.on_message(filters.command("system"))
async def system_stats(client, message):
    uptime = str(datetime.now() - datetime.fromtimestamp(boot_time)).split('.')[0]
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    sys_text = f"""🖥️ **𝗙𝗟𝗜𝗫𝗢𝗥𝗔 𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗧𝗔𝗧𝗦**
━━━━━━━━━━━━━━━━━
🕒 **Uptime:** `{uptime}`
⚙️ **CPU Usage:** `{cpu}%`
💾 **RAM Usage:** `{ram}%`
📡 **Status:** `Running Smooth 🚀`"""
    await message.reply_text(sys_text, quote=True)

# --- STARTUP ---
async def main():
    await start_web_server()
    await app.start()
    await app.set_bot_commands([
        BotCommand("start", "Open Main Menu"),
        BotCommand("id", "Get ID & Premium Status"),
        BotCommand("stickerid", "Get ID from Sticker"),
        BotCommand("getsticker", "Get Sticker from ID"),
        BotCommand("system", "Check Server Stats")
    ])
    print("Flixora Pro ID Bot is Ready!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
