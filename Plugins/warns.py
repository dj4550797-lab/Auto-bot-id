from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

WARN_LIMIT = 3

@Client.on_message(filters.command("warn") & filters.group)
async def warn_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return await message.reply_text("Reply to warn.")
    user = message.reply_to_message.from_user
    warns = await db.add_warn(message.chat.id, user.id)
    if warns >= WARN_LIMIT:
        await client.ban_chat_member(message.chat.id, user.id)
        await db.reset_warns(message.chat.id, user.id)
        await message.reply_text(f"🚫 {user.mention} reached {WARN_LIMIT} warns and was Banned!")
    else:
        await message.reply_text(f"⚠️ {user.mention} Warned! ({warns}/{WARN_LIMIT})")

@Client.on_message(filters.command(["unwarn", "rmwarn"]) & filters.group)
async def remove_warn(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    await db.reset_warns(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply_text(f"✅ Warnings reset for {message.reply_to_message.from_user.mention}.")