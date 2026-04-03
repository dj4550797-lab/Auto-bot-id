from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from utils.helpers import is_group_admin

@Client.on_message(filters.command("kick") & filters.group)
async def kick_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user.")
    user_id = message.reply_to_message.from_user.id
    await client.ban_chat_member(message.chat.id, user_id)
    await client.unban_chat_member(message.chat.id, user_id)
    await message.reply_text(f"👢 Kicked {message.reply_to_message.from_user.mention}.")

@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    user_id = message.reply_to_message.from_user.id
    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
    await message.reply_text(f"🔇 Muted {message.reply_to_message.from_user.mention}.")

@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message):
    if not await is_group_admin(client, message): return
    user_id = message.reply_to_message.from_user.id
    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
    await message.reply_text(f"🔊 Unmuted {message.reply_to_message.from_user.mention}.")

@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    await message.reply_to_message.pin()

@Client.on_message(filters.command("purge") & filters.group)
async def purge_messages(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return await message.reply_text("Reply to a message to purge.")
    start, end = message.reply_to_message.id, message.id
    await client.delete_messages(message.chat.id, [i for i in range(start, end + 1)])