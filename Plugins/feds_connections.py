import json
from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin
from uuid import uuid4

# 1. FEDERATIONS
@Client.on_message(filters.command("newfed"))
async def new_fed(client, message):
    fed_id = str(uuid4())[:8]
    name = message.text.split(" ", 1)[1] if len(message.command) > 1 else "My Fed"
    await db.create_fed(fed_id, name, message.from_user.id)
    await message.reply_text(f"🌐 **Federation Created!**\n**Name:** {name}\n**Fed ID:** `{fed_id}`")

@Client.on_message(filters.command("joinfed") & filters.group)
async def join_fed(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/joinfed [fed_id]`")
    await db.join_fed(message.chat.id, message.command[1])
    await message.reply_text(f"✅ Group linked to Federation: `{message.command[1]}`")

@Client.on_message(filters.command("fban"))
async def fban_user(client, message):
    if not message.reply_to_message: return
    fed_id = await db.get_chat_fed(message.chat.id)
    if not fed_id: return await message.reply_text("This group is not in a federation.")
    
    user_id = message.reply_to_message.from_user.id
    await db.fban_user(fed_id, user_id)
    await client.ban_chat_member(message.chat.id, user_id)
    await message.reply_text(f"🔨 **Fed-Banned!** User will be banned in all groups sharing this Fed.")

@Client.on_message(filters.new_chat_members, group=14)
async def check_fban(client, message):
    fed_id = await db.get_chat_fed(message.chat.id)
    if not fed_id: return
    for user in message.new_chat_members:
        if await db.is_fbanned(fed_id, user.id):
            await client.ban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"🚨 **Federation Ban:** {user.mention} was removed because they are banned in the Federation.")

# 2. CONNECTIONS (Edit group in PMs)
@Client.on_message(filters.command("connect") & filters.private)
async def connect_chat(client, message):
    if len(message.command) < 2: return await message.reply_text("Usage: `/connect [chat_id]`")
    await db.set_setting(message.from_user.id, "connected_chat", int(message.command[1]))
    await message.reply_text(f"🔌 Connected to `{message.command[1]}`! Commands you type here will affect the group.")

# 3. IMPORT / EXPORT (Backup)
@Client.on_message(filters.command("export") & filters.group)
async def export_data(client, message):
    if not await is_group_admin(client, message): return
    rules = await db.get_rules(message.chat.id)
    welcome = await db.get_welcome(message.chat.id)
    data = {"rules": rules, "welcome": welcome}
    
    with open(f"backup_{message.chat.id}.json", "w") as f:
        json.dump(data, f)
    await message.reply_document(f"backup_{message.chat.id}.json", caption="📦 **Group Backup**")

@Client.on_message(filters.command("import") & filters.group)
async def import_data(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message or not message.reply_to_message.document: return await message.reply_text("Reply to a JSON file.")
    
    file = await message.reply_to_message.download()
    with open(file, "r") as f:
        data = json.load(f)
    
    if data.get("rules"): await db.set_rules(message.chat.id, data["rules"])
    if data.get("welcome"): await db.set_welcome(message.chat.id, data["welcome"])
    await message.reply_text("✅ Group settings restored from backup!")