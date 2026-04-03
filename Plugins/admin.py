from pyrogram import Client, filters
from info import ADMINS
from database.db import db

# Filter to check if user is admin
async def is_admin(_, __, message):
    return message.from_user and message.from_user.id in ADMINS

admin_filter = filters.create(is_admin)

@Client.on_message(filters.command("ban") & admin_filter)
async def ban_user_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to ban them.")
    
    user_id = message.reply_to_message.from_user.id
    await db.ban_user(user_id)
    await message.reply_text(f"✅ User `{user_id}` has been banned from using the bot.")

@Client.on_message(filters.command("unban") & admin_filter)
async def unban_user_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to unban them.")
    
    user_id = message.reply_to_message.from_user.id
    await db.unban_user(user_id)
    await message.reply_text(f"✅ User `{user_id}` has been unbanned.")

@Client.on_message(filters.command("groups") & admin_filter)
async def list_groups_cmd(client, message):
    groups = await db.get_all_groups()
    if not groups:
        return await message.reply_text("I am not in any groups yet.")
        
    text = "**📊 Groups I am currently in:**\n\n"
    for grp in groups:
        text += f"▪️ `{grp['_id']}` - {grp.get('title', 'Unknown')}\n"
        
    await message.reply_text(text)