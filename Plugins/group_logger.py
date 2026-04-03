from pyrogram import Client, filters
from info import LOG_CHANNEL
from database.db import db

@Client.on_message(filters.new_chat_members)
async def on_bot_joined(client, message):
    me = await client.get_me()
    for new_member in message.new_chat_members:
        if new_member.id == me.id:
            await db.add_group(message.chat.id, message.chat.title)
            if LOG_CHANNEL:
                await client.send_message(LOG_CHANNEL, f"🎉 **Joined Group!**\n**Name:** {message.chat.title}\n**ID:** `{message.chat.id}`\n**Members:** `{message.chat.members_count}`")

@Client.on_message(filters.left_chat_member)
async def on_bot_kicked(client, message):
    me = await client.get_me()
    if message.left_chat_member.id == me.id:
        await db.remove_group(message.chat.id)
        if LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"⚠️ **Removed from Group**\n**Name:** {message.chat.title}\n**ID:** `{message.chat.id}`")