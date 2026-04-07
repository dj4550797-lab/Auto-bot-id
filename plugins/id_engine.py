from pyrogram import Client, filters
from script import Script

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        Script.START_TXT.format(first_name=message.from_user.first_name)
    )

@Client.on_message(filters.command("id"))
async def id_handler(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "N/A"
    
    # Logic for replies and forwards
    replied_id = "──"
    forward_id = "──"
    
    if message.reply_to_message:
        replied = message.reply_to_message
        if replied.from_user:
            replied_id = f"`{replied.from_user.id}`"
        
        if replied.forward_from_chat: # For Channel IDs
            forward_id = f"`{replied.forward_from_chat.id}`"
        elif replied.forward_from: # For User Forwards
            forward_id = f"`{replied.forward_from.id}`"

    text = (
        f"┏━━🆔 **IDENTITY HUB**\n"
        f"┃\n"
        f"┣🔹 **Chat ID:** `{chat_id}`\n"
        f"┣👤 **User ID:** `{user_id}`\n"
        f"┃\n"
        f"┣🎯 **Replied User:** {replied_id}\n"
        f"┣📢 **Forwarded From:** {forward_id}\n"
        f"┃\n"
        f"┗━━━━━━━✨━━━━━━━┛"
    )
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id_handler(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("⚠️ **Please reply to a sticker!**")
    
    s = message.reply_to_message.sticker
    text = (
        f"┏━━🎫 **STICKER METADATA**\n"
        f"┃\n"
        f"┣🔹 **File ID:**\n┃ `{s.file_id}`\n"
        f"┣🔹 **Unique ID:** `{s.file_unique_id}`\n"
        f"┣🔹 **Emoji:** {s.emoji}\n"
        f"┃\n"
        f"┗━━━━━━━━━━━━━━━┛"
    )
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command("help"))
async def help_handler(client, message):
    await message.reply_text(Script.HELP_TXT)
