from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges, ChatPermissions
from utils.helpers import is_group_admin, parse_time

@Client.on_message(filters.command("tban") & filters.group)
async def temp_ban(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2 or not message.reply_to_message: return await message.reply_text("Reply & use `/tban 2d`")
    until_date = parse_time(message.command[1])
    if not until_date: return await message.reply_text("Invalid time (use 1d, 5h, 30m).")
    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=until_date)
    await message.reply_text(f"🔨 Banned {message.reply_to_message.from_user.mention} for {message.command[1]}.")

@Client.on_message(filters.command("tmute") & filters.group)
async def temp_mute(client, message):
    if not await is_group_admin(client, message): return
    if len(message.command) < 2 or not message.reply_to_message: return
    until_date = parse_time(message.command[1])
    await client.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False), until_date=until_date)
    await message.reply_text(f"🔇 Muted {message.reply_to_message.from_user.mention} for {message.command[1]}.")

@Client.on_message(filters.command("promote") & filters.group)
async def promote_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    privileges = ChatPrivileges(can_manage_chat=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True)
    await client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, privileges)
    await message.reply_text(f"👑 Promoted {message.reply_to_message.from_user.mention}!")

@Client.on_message(filters.command("demote") & filters.group)
async def demote_user(client, message):
    if not await is_group_admin(client, message): return
    if not message.reply_to_message: return
    privileges = ChatPrivileges(can_manage_chat=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False)
    await client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, privileges)
    await message.reply_text(f"📉 Demoted {message.reply_to_message.from_user.mention}.")