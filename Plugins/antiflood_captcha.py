import time, random
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from utils.helpers import is_group_admin

# Trackers in memory
FLOOD_TRACKER = {}
RAID_TRACKER = {}

# 1. ANTIFLOOD & ANTIRAID
@Client.on_message(filters.command("setflood") & filters.group)
async def set_flood(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/setflood 5` (Messages per 5s)")
    await db.set_setting(message.chat.id, "flood_limit", int(message.command[1]))
    await message.reply_text(f"🌊 AntiFlood set to {message.command[1]} messages.")

@Client.on_message(filters.group & ~filters.bot, group=12)
async def flood_check(client, message):
    if await is_group_admin(client, message) or await db.is_approved(message.chat.id, message.from_user.id): return
    limit = await db.get_setting(message.chat.id, "flood_limit")
    if not limit: return
    
    chat, user = message.chat.id, message.from_user.id
    if chat not in FLOOD_TRACKER: FLOOD_TRACKER[chat] = {}
    if user not in FLOOD_TRACKER[chat]: FLOOD_TRACKER[chat][user] = []
    
    now = time.time()
    FLOOD_TRACKER[chat][user] = [t for t in FLOOD_TRACKER[chat][user] if now - t < 5] # 5 seconds window
    FLOOD_TRACKER[chat][user].append(now)
    
    if len(FLOOD_TRACKER[chat][user]) >= limit:
        await client.restrict_chat_member(chat, user, ChatPermissions(can_send_messages=False))
        await message.reply_text(f"🚫 {message.from_user.mention} was muted for flooding.")
        FLOOD_TRACKER[chat][user] = []

# 2. CAPTCHA
@Client.on_message(filters.command("captcha") & filters.group)
async def toggle_captcha(client, message):
    if not await is_group_admin(client, message): return
    current = await db.get_setting(message.chat.id, "captcha")
    await db.set_setting(message.chat.id, "captcha", not current)
    await message.reply_text(f"🤖 CAPTCHA is now **{'OFF' if current else 'ON'}**.")

@Client.on_message(filters.new_chat_members, group=13)
async def captcha_new_members(client, message):
    if not await db.get_setting(message.chat.id, "captcha"): return
    for user in message.new_chat_members:
        if user.is_bot: continue
        
        # Restrict user
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        
        # Send Button
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ I am Human", callback_data=f"capt_{user.id}")]])
        msg = await message.reply_text(f"👋 {user.mention}, please click the button below to prove you are human.", reply_markup=btn)

@Client.on_callback_query(filters.regex(r"^capt_"))
async def captcha_callback(client, query):
    user_id = int(query.data.split("_")[1])
    if query.from_user.id != user_id:
        return await query.answer("This button is not for you!", show_alert=True)
    
    await client.restrict_chat_member(query.message.chat.id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
    await query.message.delete()
    await query.answer("✅ Verified! You can now chat.")