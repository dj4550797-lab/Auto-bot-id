import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from plugins.admin_utils import is_admin

# --- BAN USER ---
@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Ye command sirf Admins use kar sakte hain!")
    
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Ban karne ke liye kisi ke message par reply karein.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(
            f"┏━━🚫 **USER BANNED**\n"
            f"┣👤 **User:** {message.reply_to_message.from_user.mention}\n"
            f"┣👮 **Admin:** {message.from_user.mention}\n"
            f"┗━━━━━━━━━━━━━┛"
        )
    except Exception as e:
        await message.reply_text(f"❌ Ban nahi kar paya. Pata karein ki mere paas Admin rights hain ya nahi.")

# --- KICK USER (Ban & Unban quickly) ---
@Client.on_message(filters.command("kick") & filters.group)
async def kick_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Ye command sirf Admins use kar sakte hain!")
        
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Kick karne ke liye kisi ke message par reply karein.")
        
    user_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await asyncio.sleep(1)
        await client.unban_chat_member(message.chat.id, user_id) # Unban so they can rejoin later
        await message.reply_text(f"👢 **{message.reply_to_message.from_user.first_name}** ko group se nikal diya gaya hai!")
    except Exception:
        await message.reply_text("❌ Kick fail ho gaya. Admin rights check karein.")

# --- MUTE USER ---
@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Sirf Admins mute kar sakte hain!")
        
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Mute karne ke liye kisi ke message par reply karein.")
        
    user_id = message.reply_to_message.from_user.id
    try:
        await client.restrict_chat_member(
            message.chat.id, user_id,
            ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"🤐 **{message.reply_to_message.from_user.first_name}** ko mute kar diya gaya hai.")
    except Exception:
        await message.reply_text("❌ Mute nahi kar paya.")

# --- UNMUTE USER ---
@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return
        
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Kisi ke message par reply karein.")
        
    user_id = message.reply_to_message.from_user.id
    try:
        await client.restrict_chat_member(
            message.chat.id, user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply_text(f"🔊 **{message.reply_to_message.from_user.first_name}** ab message bhej sakta hai.")
    except Exception:
        await message.reply_text("❌ Unmute fail hua.")

# --- PURGE (Delete Bulk Messages) ---
@Client.on_message(filters.command("purge") & filters.group)
async def purge_messages(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Admins only!")
        
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Jaha se messages delete karne hain, us message par reply karke `/purge` likhein.")
        
    start_msg_id = message.reply_to_message.id
    end_msg_id = message.id
    
    message_ids =[]
    for current_msg_id in range(start_msg_id, end_msg_id + 1):
        message_ids.append(current_msg_id)
        # Telegram API limit is 100 messages at a time
        if len(message_ids) == 100:
            await client.delete_messages(message.chat.id, message_ids)
            message_ids =[]
            await asyncio.sleep(1)
            
    if len(message_ids) > 0:
        await client.delete_messages(message.chat.id, message_ids)
        
    reply = await message.reply_text("🧹 **Purge Complete!** Messages deleted.")
    await asyncio.sleep(3)
    await reply.delete()

# --- PIN / UNPIN ---
@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to a message to pin it.")
        
    try:
        await message.reply_to_message.pin()
        await message.reply_text("📌 **Message Pinned!**")
    except Exception:
        await message.reply_text("❌ Pin nahi kar paya.")
