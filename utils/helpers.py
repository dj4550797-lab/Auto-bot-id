import time
import psutil
import re
from datetime import datetime, timedelta
from pyrogram.enums import ChatMemberStatus
from database.db import db # Import db for the new helpers

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    # ... (This function remains unchanged)
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
    for x in range(len(time_list)): time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4: ping_time += f"{time_list[3]} {time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 3: ping_time += f"{time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 2: ping_time += f"{time_list[1]} {time_list[0]}"
    elif len(time_list) == 1: ping_time += f"{time_list[0]}"
    return ping_time.strip()

def parse_time(time_str: str):
    # ... (This function remains unchanged)
    regex = re.compile(r"(\d+)(d|h|m)")
    match = regex.match(time_str)
    if not match: return None
    value, unit = int(match.group(1)), match.group(2)
    if unit == "d": delta = timedelta(days=value)
    elif unit == "h": delta = timedelta(hours=value)
    elif unit == "m": delta = timedelta(minutes=value)
    else: return None
    return datetime.now() + delta

# --- CRITICAL UPDATE: is_group_admin now accepts a chat_id ---
async def is_group_admin(client, message, chat_id: int = None) -> bool:
    """Checks if the user is an admin in the target chat."""
    target_chat_id = chat_id or message.chat.id
    if message.chat.type.name == "PRIVATE" and not target_chat_id: return False
    
    if message.sender_chat and message.sender_chat.id == target_chat_id:
        return True
    try:
        member = await client.get_chat_member(target_chat_id, message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False

# --- NEW HELPERS FOR CONNECTIONS, LOGGING, and CLEANING ---

async def get_target_chat(client, message):
    """Gets the correct chat_id for commands, supporting PM connections."""
    if message.chat.type.name == "PRIVATE":
        return await db.get_setting(message.from_user.id, "connected_chat")
    return message.chat.id

async def log_action(client, chat_id, admin_name, action, target_name):
    """Sends a log message to the group's designated log channel."""
    log_channel_id = await db.get_log_channel(chat_id)
    if log_channel_id:
        log_text = f"📝 **LOG**\n**Admin:** {admin_name}\n**Action:** {action}\n**Target:** {target_name}"
        try:
            await client.send_message(log_channel_id, log_text)
        except Exception:
            await db.set_log_channel(chat_id, None)

async def clean_command(client, message, chat_id):
    """Deletes the admin's command message if clean_commands is enabled."""
    if await db.get_setting(chat_id, "clean_commands"):
        try:
            await message.delete()
        except Exception:
            pass
`