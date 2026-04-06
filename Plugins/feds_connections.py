import json
import os
from uuid import uuid4
from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin

# --- 1. FEDERATIONS ---

@Client.on_message(filters.command("newfed") & filters.private)
async def new_fed(client, message):
    """Creates a new Federation (Private only to avoid spam)"""
    fed_id = str(uuid4())[:8]
    name = message.text.split(" ", 1)[1] if len(message.command) > 1 else f"{message.from_user.first_name}'s Fed"
    
    await db.create_fed(fed_id, name, message.from_user.id)
    await message.reply_text(
        f"🌐 **Federation Created!**\n\n"
        f"**Name:** {name}\n"
        f"**Fed ID:** `{fed_id}`\n\n"
        f"Use `/joinfed {fed_id}` in your groups to link them."
    )

@Client.on_message(filters.command("joinfed") & filters.group)
async def join_fed(client, message):
    """Joins a group to a specific Federation"""
    if not await is_group_admin(client, message):
        return
        
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/joinfed [fed_id]`")
    
    fed_id = message.command[1]
    # In a production bot, you'd verify if the fed_id exists here.
    await db.join_fed(message.chat.id, fed_id)
    await message.reply_text(f"✅ Group successfully linked to Federation: `{fed_id}`")

@Client.on_message(filters.command("fban") & filters.group)
async def fban_user(client, message):
    """Bans a user across all groups in the federation"""
    if not await is_group_admin(client, message):
        return
        
    fed_id = await db.get_chat_fed(message.chat.id)
    if not fed_id:
        return await message.reply_text("❌ This group is not part of any Federation.")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to Federation Ban them.")
    
    user = message.reply_to_message.from_user
    await db.fban_user(fed_id, user.id)
    
    # Ban in current group immediately
    try:
        await client.ban_chat_member(message.chat.id, user.id)
    except:
        pass
        
    await message.reply_text(f"🔨 **Fed-Banned!**\n{user.mention} has been banned across the Federation: `{fed_id}`.")

@Client.on_message(filters.new_chat_members, group=14)
async def check_fban(client, message):
    """Auto-kick users who are Fed-Banned when they join"""
    fed_id = await db.get_chat_fed(message.chat.id)
    if not fed_id:
        return
        
    for user in message.new_chat_members:
        if await db.is_fbanned(fed_id, user.id):
            try:
                await client.ban_chat_member(message.chat.id, user.id)
                await message.reply_text(f"🚨 **Federation Ban Found:** {user.mention} was removed.")
            except Exception:
                pass

# --- 2. IMPORT / EXPORT (GROUP SETTINGS BACKUP) ---

@Client.on_message(filters.command("export") & filters.group)
async def export_data(client, message):
    """Exports Rules and Welcome text to a JSON file"""
    if not await is_group_admin(client, message):
        return
        
    rules = await db.get_rules(message.chat.id)
    welcome = await db.get_welcome(message.chat.id)
    
    data = {
        "chat_id": message.chat.id,
        "rules": rules,
        "welcome": welcome
    }
    
    file_path = f"backup_{message.chat.id}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    await message.reply_document(file_path, caption=f"📦 **Backup for {message.chat.title}**")
    os.remove(file_path) # Clean up local storage

@Client.on_message(filters.command("import") & filters.group)
async def import_data(client, message):
    """Restores Rules and Welcome text from a JSON file"""
    if not await is_group_admin(client, message):
        return
        
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("Reply to a backup JSON file to restore settings.")
    
    # Basic security check for file extension
    if not message.reply_to_message.document.file_name.endswith(".json"):
        return await message.reply_text("Invalid file type. Please provide a `.json` backup.")

    file = await message.reply_to_message.download()
    try:
        with open(file, "r") as f:
            data = json.load(f)
        
        if data.get("rules"):
            await db.set_rules(message.chat.id, data["rules"])
        if data.get("welcome"):
            await db.set_welcome(message.chat.id, data["welcome"])
            
        await message.reply_text("✅ Settings restored successfully from backup!")
    except Exception as e:
        await message.reply_text(f"❌ Error importing data: {e}")
    finally:
        if os.path.exists(file):
            os.remove(file)
