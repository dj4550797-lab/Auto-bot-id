from pyrogram import Client, filters
from database.db import db
from utils.helpers import is_group_admin, get_target_chat, log_action

# 1. CONNECTIONS
@Client.on_message(filters.command("connect") & filters.private)
async def connect_chat(client, message):
    if len(message.command) < 2: return await message.reply_text("Usage: `/connect [chat_id]`")
    try:
        chat_id = int(message.command[1])
        chat = await client.get_chat(chat_id)
        # Check if user is admin in that chat
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [client.enums.ChatMemberStatus.ADMINISTRATOR, client.enums.ChatMemberStatus.OWNER]:
            return await message.reply_text("You are not an admin in that group!")
        
        await db.set_setting(message.from_user.id, "connected_chat", chat_id)
        await message.reply_text(f"🔌 Successfully connected to **{chat.title}**!")
    except Exception as e:
        await message.reply_text(f"Error connecting: {e}")

@Client.on_message(filters.command("disconnect") & filters.private)
async def disconnect_chat(client, message):
    await db.set_setting(message.from_user.id, "connected_chat", None)
    await message.reply_text("🔌 Disconnected from chat.")

# 2. LOG CHANNELS
@Client.on_message(filters.command("setlog") & filters.group)
async def set_log(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/setlog [channel_id]`")
    
    log_channel_id = int(message.command[1])
    await db.set_log_channel(message.chat.id, log_channel_id)
    await message.reply_text(f"✅ Log channel set to `{log_channel_id}`")

# 3. DISABLING COMMANDS
@Client.on_message(filters.command("disable") & filters.group)
async def disable_cmd(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("Usage: `/disable [command]`")
    
    cmd = message.command[1].lower()
    await db.disable_command(message.chat.id, cmd)
    await message.reply_text(f"❌ Command `/{cmd}` has been disabled.")

@Client.on_message(filters.command("enable") & filters.group)
async def enable_cmd(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2: return
    
    cmd = message.command[1].lower()
    await db.enable_command(message.chat.id, cmd)
    await message.reply_text(f"✅ Command `/{cmd}` has been enabled.")

# Filter to check for disabled commands
@Client.on_message(filters.group, group=100)
async def check_disabled(client, message):
    if message.text and message.text.startswith("/"):
        cmd = message.text.split(" ")[0][1:].lower()
        if await db.is_disabled(message.chat.id, cmd):
            await message.delete()

# 4. CLEAN COMMANDS
@Client.on_message(filters.command("cleancommands") & filters.group)
async def clean_cmds_toggle(client, message):
    if not await is_group_admin(client, message): return
    current_status = await db.get_setting(message.chat.id, "clean_commands")
    await db.set_setting(message.chat.id, "clean_commands", not current_status)
    await message.reply_text(f"🧹 Clean Commands is now **{'OFF' if current_status else 'ON'}**.")