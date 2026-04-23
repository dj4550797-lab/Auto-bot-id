from pyrogram import Client, filters
from pyrogram.types import Message
from info import LOG_CHANNEL

# Track new users sending /start
@Client.on_message(filters.command("start") & filters.private, group=2)
async def log_new_user(client, message: Message):
    if LOG_CHANNEL != 0:
        user = message.from_user
        log_text = (
            f"**👤 #NEW_USER_STARTED**\n\n"
            f"**Name:** {user.mention}\n"
            f"**ID:** `{user.id}`\n"
            f"**Username:** @{user.username if user.username else 'N/A'}"
        )
        try:
            await client.send_message(LOG_CHANNEL, log_text)
        except Exception:
            pass

# Track when bot is added to a new Group
@Client.on_message(filters.new_chat_members, group=2)
async def log_new_group(client, message: Message):
    if LOG_CHANNEL != 0:
        for member in message.new_chat_members:
            if member.is_self: # Bot was added
                chat = message.chat
                adder = message.from_user
                log_text = (
                    f"**🥳 #BOT_ADDED_TO_GROUP**\n\n"
                    f"**Group Name:** {chat.title}\n"
                    f"**Group ID:** `{chat.id}`\n"
                    f"**Added By:** {adder.mention} (`{adder.id}`)\n"
                    f"**Total Members:** {await client.get_chat_members_count(chat.id)}"
                )
                try:
                    await client.send_message(LOG_CHANNEL, log_text)
                except Exception:
                    pass

# Track whenever someone searches for an ID
@Client.on_message(filters.command(["id", "stid"]) & filters.private, group=2)
async def log_searches(client, message: Message):
    if LOG_CHANNEL != 0:
        user = message.from_user
        log_text = (
            f"**🔍 #ID_SEARCHED**\n\n"
            f"**User:** {user.mention} (`{user.id}`)\n"
            f"**Command Used:** {message.text}"
        )
        try:
            await client.send_message(LOG_CHANNEL, log_text)
        except Exception:
            pass
