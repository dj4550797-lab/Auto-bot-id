from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

@Client.on_message(filters.command("setrules") & filters.group)
async def set_group_rules(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/setrules [rules]`")
    await db.set_rules(message.chat.id, message.text.markdown.split(" ", 1)[1])
    await message.reply_text("✅ Rules updated!")

@Client.on_message(filters.command("rules") & filters.group)
async def get_group_rules(client, message):
    rules = await db.get_rules(message.chat.id)
    if rules: await message.reply_text(f"📜 **Rules:**\n\n{rules}", disable_web_page_preview=True)
    else: await message.reply_text("No rules set.")

@Client.on_message(filters.command("save") & filters.group)
async def save_note(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 3: return await message.reply_text("Usage: `/save [name] [text]`")
    name = message.command[1].lower()
    await db.save_note(message.chat.id, name, message.text.markdown.split(" ", 2)[2])
    await message.reply_text(f"✅ Note saved! Use `#{name}`")

@Client.on_message(filters.regex(r"^#(\w+)") & filters.group, group=3)
async def regex_get_note(client, message):
    note = await db.get_note(message.chat.id, message.matches[0].group(1).lower())
    if note: await message.reply_text(note, quote=True)