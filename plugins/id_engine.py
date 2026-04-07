from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from script import Script

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("❓ ID Kaise Dhundhein?", callback_data="how_to")
    ]])
    await message.reply_text(
        Script.START_TXT.format(first_name=message.from_user.first_name),
        reply_markup=btn
    )

@Client.on_message(filters.command("how"))
async def how_handler(client, message):
    await message.reply_text(Script.HOW_TO_TXT)

@Client.on_callback_query(filters.regex("how_to"))
async def cb_how(client, query):
    await query.message.edit_text(Script.HOW_TO_TXT)

@Client.on_message(filters.command("id"))
async def smart_id(client, message):
    # Case 1: Reply to a Forward (Channel ID)
    if message.reply_to_message and message.reply_to_message.forward_from_chat:
        target = message.reply_to_message.forward_from_chat
        text = f"┏━━📢 **CHANNEL ID**\n┣🔹 **Name:** `{target.title}`\n┣🆔 **ID:** `{target.id}`\n┗━━━━━━━━━━━━━┛"
    
    # Case 2: Reply to a User Message (User ID)
    elif message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            return await message.reply_text("⚠️ User ki details nahi mil saki (Privacy Settings).")
        text = f"┏━━👤 **USER ID**\n┣🔹 **Name:** {user.mention}\n┣🆔 **ID:** `{user.id}`\n┗━━━━━━━━━━━━━┛"
    
    # Case 3: Normal command (Chat/Group ID)
    else:
        text = f"┏━━👥 **CHAT ID**\n┣🔹 **Title:** `{message.chat.title or 'Private'}`\n┣🆔 **ID:** `{message.chat.id}`\n┗━━━━━━━━━━━━━┛"
    
    await message.reply_text(text, quote=True)

@Client.on_message(filters.command(["stickerid", "stid"]))
async def get_stid(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("⚠️ Sticker par reply karke `/stid` likhein!")
    
    s = message.reply_to_message.sticker
    await message.reply_text(
        f"┏━━🎫 **STICKER ID**\n┣🆔 `{s.file_id}`\n┗━━━━━━━━━━━━━┛",
        quote=True
    )

@Client.on_message(filters.command("getsticker"))
async def id_to_sticker(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **Usage:** `/getsticker [file_id]`")
    
    file_id = message.command[1]
    try:
        await message.reply_sticker(file_id)
    except Exception as e:
        await message.reply_text(f"❌ **Invalid ID ya Error:** `{e}`")
