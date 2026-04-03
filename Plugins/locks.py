from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

LOCK_TYPES = ["url", "forward", "sticker", "photo", "video"]

@Client.on_message(filters.command("lock") & filters.group)
async def lock_module(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2 or message.command[1].lower() not in LOCK_TYPES: return await message.reply_text(f"Available: {', '.join(LOCK_TYPES)}")
    await db.update_lock(message.chat.id, message.command[1].lower(), True)
    await message.reply_text(f"🔒 Locked `{message.command[1].lower()}`")

@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_module(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return
    await db.update_lock(message.chat.id, message.command[1].lower(), False)
    await message.reply_text(f"🔓 Unlocked `{message.command[1].lower()}`")

@Client.on_message(filters.group & ~filters.bot, group=4)
async def check_locks(client, message):
    if await is_group_admin(client, message): return
    locks = await db.get_locks(message.chat.id)
    if not locks: return
    should_delete = False
    
    if locks.get("url") and (message.entities or message.caption_entities):
        for ent in (message.entities or message.caption_entities):
            if ent.type.name in ["URL", "TEXT_LINK"]: should_delete = True
            
    if locks.get("forward") and (message.forward_from_chat or message.forward_from): should_delete = True
    if locks.get("sticker") and message.sticker: should_delete = True
    if locks.get("photo") and message.photo: should_delete = True
    if locks.get("video") and message.video: should_delete = True
    
    if should_delete:
        try: await message.delete()
        except: pass