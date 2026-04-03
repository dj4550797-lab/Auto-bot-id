from pyrogram import Client, filters
from pyrogram.types import Message
from info import LOG_CHANNEL
from database.db import db

@Client.on_message(filters.new_chat_members)
async def on_bot_joined(client, message: Message):
    # Check if the bot itself was added
    me = await client.get_me()
    for new_member in message.new_chat_members:
        if new_member.id == me.id:
            # Add to Database
            await db.add_group(message.chat.id, message.chat.title)
            
            # Send Log to Channel
            if LOG_CHANNEL:
                log_text = (
                    f"🎉 **Bot Added To New Group!**\n\n"
                    f"**Group Name:** {message.chat.title}\n"
                    f"**Group ID:** `{message.chat.id}`\n"
                    f"**Added By:** {message.from_user.mention}\n"
                    f"**Members Count:** `{message.chat.members_count}`"
                )
                await client.send_message(LOG_CHANNEL, log_text)

@Client.on_message(filters.left_chat_member)
async def on_bot_kicked(client, message: Message):
    me = await client.get_me()
    if message.left_chat_member.id == me.id:
        # Remove from Database
        await db.remove_group(message.chat.id)
        
        # Send Log to Channel
        if LOG_CHANNEL:
            log_text = (
                f"⚠️ **Bot Removed From Group**\n\n"
                f"**Group Name:** {message.chat.title}\n"
                f"**Group ID:** `{message.chat.id}`"
            )
            await client.send_message(LOG_CHANNEL, log_text)