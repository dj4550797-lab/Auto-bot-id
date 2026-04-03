from pyrogram import Client, filters
from database.db import db

@Client.on_message(filters.command("id"))
async def get_id(client, message):
    if await db.is_banned(message.from_user.id): return
    text = f"**📌 Chat ID:** `{message.chat.id}`\n"
    if message.from_user:
        text += f"**👤 User ID:** `{message.from_user.id}` (Premium: {'✅' if message.from_user.is_premium else '❌'})\n"
    if message.reply_to_message:
        replied = message.reply_to_message
        if replied.from_user: text += f"**🎯 Replied ID:** `{replied.from_user.id}`\n"
        if replied.forward_from: text += f"**↪️ Forwarded User ID:** `{replied.forward_from.id}`\n"
        elif replied.forward_from_chat: text += f"**📢 Forwarded Channel ID:** `{replied.forward_from_chat.id}`\n"
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command(["stickerid", "stid"]))
async def get_sticker_id(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker: return await message.reply_text("⚠️ Reply to a sticker!")
    s = message.reply_to_message.sticker
    await message.reply_text(f"**File ID:** `{s.file_id}`\n**Unique ID:** `{s.file_unique_id}`\n**Premium:** {'✅' if s.is_premium else '❌'}", quote=True)