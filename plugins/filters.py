from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.admin_utils import is_admin

# Memory mein filters save karne ke liye dictionary
GROUP_FILTERS = {}

@Client.on_message(filters.command("filter") & filters.group)
async def add_filter(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Sirf admins filter laga sakte hain.")
        
    if len(message.command) < 3:
        return await message.reply_text("❌ **Usage:** `/filter[keyword] [reply message]`\nExample: `/filter rule Padhai par dhyan do!`")
        
    chat_id = message.chat.id
    keyword = message.command[1].lower()
    reply_text = message.text.split(None, 2)[2]
    
    if chat_id not in GROUP_FILTERS:
        GROUP_FILTERS[chat_id] = {}
        
    GROUP_FILTERS[chat_id][keyword] = reply_text
    await message.reply_text(f"✅ Filter added!\nJab bhi koi `{keyword}` likhega, main reply karunga.")

@Client.on_message(filters.command("stop") & filters.group)
async def stop_filter(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return
        
    if len(message.command) < 2:
        return await message.reply_text("❌ **Usage:** `/stop [keyword]`")
        
    chat_id = message.chat.id
    keyword = message.command[1].lower()
    
    if chat_id in GROUP_FILTERS and keyword in GROUP_FILTERS[chat_id]:
        del GROUP_FILTERS[chat_id][keyword]
        await message.reply_text(f"🗑️ Filter `{keyword}` delete kar diya gaya.")
    else:
        await message.reply_text("⚠️ Aisa koi filter is group mein nahi hai.")

# Triggering the filter
@Client.on_message(filters.text & filters.group, group=3)
async def catch_filter(client, message: Message):
    chat_id = message.chat.id
    if chat_id in GROUP_FILTERS:
        text = message.text.lower()
        for keyword, reply in GROUP_FILTERS[chat_id].items():
            if keyword in text.split():
                await message.reply_text(reply)
                break
