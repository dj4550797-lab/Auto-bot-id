from pyrogram import Client, filters
from database.db import db

@Client.on_message(filters.command("id"))
async def get_id(client, message):
    if await db.is_banned(message.from_user.id):
        return
        
    text = f"**📌 Current Chat ID:** `{message.chat.id}`\n"
    text += f"**💬 Chat Type:** `{message.chat.type.name}`\n\n"
    
    # User Info
    if message.from_user:
        premium_status = "✅ Yes" if message.from_user.is_premium else "❌ No"
        dc_id = message.from_user.dc_id or "Unknown"
        text += (
            f"**👤 User Info:**\n"
            f" ├ **Name:** {message.from_user.first_name}\n"
            f" ├ **ID:** `{message.from_user.id}`\n"
            f" ├ **Premium:** {premium_status}\n"
            f" └ **DC ID:** `{dc_id}`\n\n"
        )
    
    # Replied Message Info
    if message.reply_to_message:
        replied = message.reply_to_message
        
        # Replied User
        if replied.from_user:
            is_prem = "✅ Yes" if replied.from_user.is_premium else "❌ No"
            text += (
                f"**🎯 Replied User:**\n"
                f" ├ **ID:** `{replied.from_user.id}`\n"
                f" └ **Premium:** {is_prem}\n\n"
            )
            
        # Forwarded Channel / User
        if replied.forward_from:
            text += f"**↪️ Forwarded User ID:** `{replied.forward_from.id}`\n"
        elif replied.forward_from_chat:
            text += f"**📢 Forwarded Channel ID:** `{replied.forward_from_chat.id}`\n"
            text += f"**📢 Channel Username:** `@{replied.forward_from_chat.username}`\n"
            
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command(["stickerid", "stid"]))
async def get_sticker_id(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("⚠️ Reply to a sticker!")
        
    sticker = message.reply_to_message.sticker
    premium_sticker = "✅ Yes" if sticker.is_premium else "❌ No"
    
    text = (
        f"**🎟 Sticker Info**\n\n"
        f"**File ID:**\n`{sticker.file_id}`\n\n"
        f"**Unique ID:**\n`{sticker.file_unique_id}`\n\n"
        f"**Premium Sticker:** {premium_sticker}"
    )
    await message.reply_text(text, quote=True)