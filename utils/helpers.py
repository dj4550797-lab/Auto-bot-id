import time
import psutil
import re
from datetime import datetime, timedelta
from pyrogram.enums import ChatMemberStatus

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
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

async def is_group_admin(client, message) -> bool:
    if message.chat.type.name == "PRIVATE": return False
    if message.sender_chat and message.sender_chat.id == message.chat.id: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False

def parse_time(time_str: str):
    regex = re.compile(r"(\d+)(d|h|m)")
    match = regex.match(time_str)
    if not match: return None
    value, unit = int(match.group(1)), match.group(2)
    if unit == "d": delta = timedelta(days=value)
    elif unit == "h": delta = timedelta(hours=value)
    elif unit == "m": delta = timedelta(minutes=value)
    else: return None
    return datetime.now() + delta