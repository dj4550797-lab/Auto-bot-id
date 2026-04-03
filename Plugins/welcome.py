from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

@Client.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2 and not message.reply_to_message: return await message.reply_text("Usage: `/setwelcome Hello {mention}`")
    text = message.text.markdown.split(" ", 1)[1] if len(message.command) > 1 else message.reply_to_message.text.markdown
    await db.set_welcome(message.chat.id, text)
    await message.reply_text("✅ Welcome saved!")

@Client.on_message(filters.new_chat_members)
async def send_welcome(client, message):
    welcome_text = await db.get_welcome(message.chat.id)
    if not welcome_text: return
    for new_member in message.new_chat_members:
        if new_member.id == (await client.get_me()).id: continue
        text = welcome_text.format(mention=new_member.mention, name=new_member.first_name, group=message.chat.title)
        await message.reply_text(text, disable_web_page_preview=True)