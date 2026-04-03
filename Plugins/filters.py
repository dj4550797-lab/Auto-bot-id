from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

@Client.on_message(filters.command("filter") & filters.group)
async def add_custom_filter(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 3: return await message.reply_text("Usage: `/filter [word] [reply]`")
    await db.add_filter(message.chat.id, message.command[1].lower(), message.text.markdown.split(" ", 2)[2])
    await message.reply_text(f"✅ Filter added for `{message.command[1]}`!")

@Client.on_message(filters.command("stop") & filters.group)
async def remove_custom_filter(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return
    await db.remove_filter(message.chat.id, message.command[1].lower())
    await message.reply_text(f"🗑 Filter removed for `{message.command[1]}`!")

@Client.on_message(filters.group & filters.text & ~filters.bot, group=2)
async def check_filters(client, message):
    chat_filters = await db.get_filters(message.chat.id)
    if not chat_filters: return
    text = message.text.lower()
    for f in chat_filters:
        if f["word"] in text:
            await message.reply_text(f["reply"], quote=True)
            break