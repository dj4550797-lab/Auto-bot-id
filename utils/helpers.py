import time
import psutil

# Bot Start Time for Uptime
START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list[3]} {time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 3:
        ping_time += f"{time_list[2]} {time_list[1]} {time_list[0]}"
    elif len(time_list) == 2:
        ping_time += f"{time_list[1]} {time_list[0]}"
    elif len(time_list) == 1:
        ping_time += f"{time_list[0]}"
    return ping_time

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    uptime = get_readable_time(time.time() - START_TIME)
    return f"**CPU:** `{cpu}%`\n**RAM:** `{ram}%`\n**Uptime:** `{uptime}`"
