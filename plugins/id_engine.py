from pyrogram import Client, filters
from script import Script

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        Script.START_TXT.format(first_name=message.from_user.first_name)
    )

@Client.on_message(filters.command("id"))
async def get_ids(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "N/A"
    replied_id = "None"
    forward_id = "None"

    if message.reply_to_message:
        replied = message.reply_to_message
        if replied.from_user:
            replied_id = replied.from_user.id
        if replied.forward_from_chat:
            forward_id = replied.forward_from_chat.id
        elif replied.forward_from:
            forward_id = replied.forward_from.id

    await message.reply_text(
        Script.ID_TXT.format(
            chat_id=chat_id,
            user_id=user_id,
            replied_id=replied_id,
            forward_id=forward_id
        )
    )

@Client.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("⚠️ **Please reply to a sticker!**")
    
    s = message.reply_to_message.sticker
    text = (
        f"┏━━🎫 **STICKER DATA**\n"
        f"┣🔹 **File ID:** `{s.file_id}`\n"
        f"┣🔹 **Unique ID:** `{s.file_unique_id}`\n"
        f"┣🔹 **Emoji:** {s.emoji}\n"
        f"┗━━━━━━━━━━━━━━━┛"
    )
    await message.reply_text(text)
