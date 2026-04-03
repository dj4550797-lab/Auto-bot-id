from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

# 1. CLEAN SERVICE (Deletes "User Joined" messages)
@Client.on_message(filters.service & filters.group, group=10)
async def clean_service_messages(client, message):
    if await db.get_setting(message.chat.id, "clean_service"):
        try: await message.delete()
        except: pass

@Client.on_message(filters.command("cleanservice") & filters.group)
async def toggle_clean_service(client, message):
    if not await is_group_admin(client, message): return
    current = await db.get_setting(message.chat.id, "clean_service")
    await db.set_setting(message.chat.id, "clean_service", not current)
    await message.reply_text(f"🧹 Clean Service is now **{'OFF' if current else 'ON'}**.")

# 2. APPROVALS (Bypass locks)
@Client.on_message(filters.command("approve") & filters.group)
async def approve_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user.")
    user = message.reply_to_message.from_user
    await db.approve_user(message.chat.id, user.id)
    await message.reply_text(f"✅ {user.mention} is now Approved! They bypass locks and antiflood.")

@Client.on_message(filters.command("unapprove") & filters.group)
async def unapprove_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    user = message.reply_to_message.from_user
    await db.unapprove_user(message.chat.id, user.id)
    await message.reply_text(f"❌ {user.mention} is no longer Approved.")

# 3. BLOCKLISTS (Auto delete bad words)
@Client.on_message(filters.command("addblock") & filters.group)
async def add_blocklist(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/addblock [word]`")
    word = message.command[1].lower()
    await db.add_blocklist(message.chat.id, word)
    await message.reply_text(f"🚫 Added `{word}` to blocklist.")

@Client.on_message(filters.text & filters.group, group=11)
async def check_blocklist(client, message):
    if await is_group_admin(client, message) or await db.is_approved(message.chat.id, message.from_user.id): return
    bad_words = await db.get_blocklist(message.chat.id)
    if any(word in message.text.lower() for word in bad_words):
        try: await message.delete()
        except: pass

# 4. REPORTS (@admin)
@Client.on_message(filters.regex(r"(?i)@admin") & filters.group)
async def report_admin(client, message):
    admins = []
    async for admin in client.get_chat_members(message.chat.id, filter=client.enums.ChatMembersFilter.ADMINISTRATORS):
        if not admin.user.is_bot: admins.append(admin.user.mention)
    if admins:
        await message.reply_text(f"🚨 **Reported to Admins!**\n{' '.join(admins)}")