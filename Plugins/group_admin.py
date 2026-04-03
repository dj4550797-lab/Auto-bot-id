from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from utils.helpers import is_group_admin, get_target_chat, log_action, clean_command

@Client.on_message(filters.command("kick"))
async def kick_user(client, message):
    chat_id = await get_target_chat(client, message)
    if not chat_id or not await is_group_admin(client, message, chat_id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user to kick.")
    
    user = message.reply_to_message.from_user
    await client.ban_chat_member(chat_id, user.id)
    await client.unban_chat_member(chat_id, user.id)
    await message.reply_text(f"👢 Kicked {user.mention}.")
    
    await log_action(client, chat_id, message.from_user.mention, "Kick", user.mention)
    await clean_command(client, message, chat_id)

@Client.on_message(filters.command("mute"))
async def mute_user(client, message):
    chat_id = await get_target_chat(client, message)
    if not chat_id or not await is_group_admin(client, message, chat_id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user to mute.")
        
    user = message.reply_to_message.from_user
    await client.restrict_chat_member(chat_id, user.id, ChatPermissions(can_send_messages=False))
    await message.reply_text(f"🔇 Muted {user.mention}.")
    
    await log_action(client, chat_id, message.from_user.mention, "Mute", user.mention)
    await clean_command(client, message, chat_id)

@Client.on_message(filters.command("unmute"))
async def unmute_user(client, message):
    chat_id = await get_target_chat(client, message)
    if not chat_id or not await is_group_admin(client, message, chat_id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user to unmute.")
    
    user = message.reply_to_message.from_user
    await client.restrict_chat_member(chat_id, user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
    await message.reply_text(f"🔊 Unmuted {user.mention}.")
    
    await log_action(client, chat_id, message.from_user.mention, "Unmute", user.mention)
    await clean_command(client, message, chat_id)

@Client.on_message(filters.command("pin"))
async def pin_message(client, message):
    chat_id = await get_target_chat(client, message)
    if not chat_id or not await is_group_admin(client, message, chat_id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a message to pin.")
    
    await message.reply_to_message.pin()
    await message.reply_text("📌 Message Pinned!")
    
    await log_action(client, chat_id, message.from_user.mention, "Pin", f"Message ID {message.reply_to_message.id}")
    await clean_command(client, message, chat_id)

@Client.on_message(filters.command("purge"))
async def purge_messages(client, message):
    chat_id = await get_target_chat(client, message)
    if not chat_id or not await is_group_admin(client, message, chat_id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a message to start purging.")
    
    start_msg_id = message.reply_to_message.id
    end_msg_id = message.id
    message_ids = [msg_id for msg_id in range(start_msg_id, end_msg_id + 1)]
    
    await client.delete_messages(chat_id, message_ids)
    
    await log_action(client, chat_id, message.from_user.mention, "Purge", f"{len(message_ids)} messages")
    # Clean command is not needed as the purge already deleted it.