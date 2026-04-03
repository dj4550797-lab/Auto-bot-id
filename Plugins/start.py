from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from script import Script
from utils.helpers import get_readable_time, START_TIME
import psutil, time

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if await db.is_banned(message.from_user.id): return await message.reply_text(Script.BANNED_TXT)
    text = Script.START_TXT.format(first_name=message.from_user.first_name)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🛠 Help", callback_data="help"), InlineKeyboardButton("🤖 About", callback_data="about")]])
    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@Client.on_message(filters.command("alive"))
async def alive_cmd(client, message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    uptime = get_readable_time(int(time.time() - START_TIME))
    await message.reply_text(Script.ALIVE_TXT.format(cpu=cpu, ram=ram, uptime=uptime), quote=True)

@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data == "help":
        await query.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif query.data == "about":
        await query.message.edit_text(Script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif query.data == "start":
        text = Script.START_TXT.format(first_name=query.from_user.first_name)
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🛠 Help", callback_data="help"), InlineKeyboardButton("🤖 About", callback_data="about")]])
        await query.message.edit_text(text, reply_markup=buttons)