from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.helpers import get_system_stats
from database.db import db
from script import Script  # Importing our long texts!

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    # Check if user is banned
    if await db.is_banned(message.from_user.id):
        return await message.reply_text(Script.BANNED_TXT)
        
    # Formatting the start text with the user's name
    text = Script.START_TXT.format(first_name=message.from_user.first_name)
    
    # Adding Inline Buttons for a premium look
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛠 Help", callback_data="help"),
            InlineKeyboardButton("🤖 About", callback_data="about")
        ]
    ])
    
    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    if await db.is_banned(message.from_user.id):
        return
    await message.reply_text(Script.HELP_TXT, quote=True)

@Client.on_message(filters.command("about") & filters.private)
async def about_cmd(client, message):
    if await db.is_banned(message.from_user.id):
        return
    await message.reply_text(Script.ABOUT_TXT, quote=True)

@Client.on_message(filters.command("alive"))
async def alive_cmd(client, message):
    import psutil, time
    from utils.helpers import START_TIME, get_readable_time
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    uptime = get_readable_time(time.time() - START_TIME)
    
    # Using the ALIVE template from script.py
    text = Script.ALIVE_TXT.format(cpu=cpu, ram=ram, uptime=uptime)
    await message.reply_text(text, quote=True)

# Callback Query Handler for the Inline Buttons
@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data == "help":
        await query.message.edit_text(
            text=Script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
        )
    elif query.data == "about":
        await query.message.edit_text(
            text=Script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]),
            disable_web_page_preview=True
        )
    elif query.data == "start":
        text = Script.START_TXT.format(first_name=query.from_user.first_name)
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🛠 Help", callback_data="help"),
                InlineKeyboardButton("🤖 About", callback_data="about")
            ]
        ])
        await query.message.edit_text(text=text, reply_markup=buttons, disable_web_page_preview=True)