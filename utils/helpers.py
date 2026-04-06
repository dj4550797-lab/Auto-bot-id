import time
import psutil
import re
from datetime import datetime, timedelta
from pyrogram.enums import ChatMemberStatus
from database.db import db

# Track when the bot started for the /alive command
START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    """Converts seconds into a human-readable format (e.g., 2d 5h 10m)."""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0: break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)): 
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4: ping_time += f"{time_list[3]} {time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 3: ping_time += f"{time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 2: ping_time += f"{time_list[1]} {time_list[0]}"
    elif len(time_list) == 1: ping_time += f"{time_list[0]}"
    return ping_time.strip()

def parse_time(time_str: str):
    """Parses time strings like '1d', '5h', '30m' for temp-bans/mutes."""
    regex = re.compile(r"(\d+)(d|h|m)")
    match = regex.match(time_str.lower())
    if not match: return None
    value, unit = int(match.group(1)), match.group(2)
    if unit == "d": delta = timedelta(days=value)
    elif unit == "h": delta = timedelta(hours=value)
    elif unit == "m": delta = timedelta(minutes=value)
    else: return None
    return datetime.now() + delta

async def is_group_admin(client, message, chat_id: int = None) -> bool:
    """
    Checks if the user is an admin. 
    Supports checking in the current chat or a specific 'chat_id'.
    """
    target_chat_id = chat_id or message.chat.id
    
    # In Private messages, if no specific chat_id is provided, return False
    if message.chat.type.name == "PRIVATE" and not chat_id: 
        return False
    
    # Handle Anonymous Admins or Channel posts
    if not message.from_user:
        if message.sender_chat and message.sender_chat.id == target_chat_id:
            return True
        return False

    try:
        member = await client.get_chat_member(target_chat_id, message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False

async def get_target_chat(client, message):
    """
    Determines which chat a command should apply to.
    If used in PM, it checks if the user has /connect-ed to a group.
    """
    if message.chat.type.name == "PRIVATE":
        connected_id = await db.get_setting(message.from_user.id, "connected_chat")
        if not connected_id:
            await message.reply_text("❌ You are not connected to any chat! Use `/connect [chat_id]` in PM.")
            return None
        return connected_id
    return message.chat.id

async def log_action(client, chat_id, admin_name, action, target_name):
    """Sends a formatted log message to the group's custom log channel."""
    log_channel_id = await db.get_log_channel(chat_id)
    if log_channel_id:
        log_text = (
            f"📝 **MOD LOG**\n"
            f"**Admin:** {admin_name}\n"
            f"**Action:** {action}\n"
            f"**Target:** {target_name}\n"
            f"**Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M')}`"
        )
        try:
            await client.send_message(log_channel_id, log_text)
        except Exception:
            # If bot can't send message (kicked/no perms), unset the log channel
            await db.set_log_channel(chat_id, None)

async def clean_command(client, message, chat_id):
    """Deletes the user's command message if 'Clean Commands' is enabled in settings."""
    if await db.get_setting(chat_id, "clean_commands"):
        try:
            await message.delete()
        except Exception:
            pass
