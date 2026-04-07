class Script(object):
    START_TXT = """
┏━━📦 **FLIXORA ADVANCED**
┃
┣👤 **Hello** {first_name}
┣🤖 **Status:** `Active & Shielded` 🛡️
┃
┣📜 **Brief:** I am a high-speed
┃ Management Bot with Global Ban
┃ & Advanced Security features.
┃
┣⚡ **Powered by:** `Pyrogram`
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    HELP_TXT = """
┏━━🛠️ **CONTROL PANEL**
┃
┣📜 **Admin Tools:**
┃ `/ban`, `/mute`, `/kick`, `/purge`
┃ `/promote`, `/pin`, `/setlog`
┃
┣🛡️ **Security:**
┃ `/antiflood` (limit), `/captcha` (on/off)
┃ `/cleanservice` (on/off), `/lock`
┃
┣🌐 **Federation:**
┃ `/newfed`, `/joinfed`, `/fban`
┃
┣📂 **Extras:**
┃ `/id`, `/stickerid`, `/save`, `/filter`
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    ALIVE_TXT = """
┏━━⚡ **SYSTEM STATUS**
┃
┣🔋 **CPU:** `{cpu}%`
┣📟 **RAM:** `{ram}%`
┣⏱️ **UPTIME:** `{uptime}`
┣🛰️ **PING:** `{ping}ms`
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    BAN_TXT = """
┏━🛡️ **ACTION: BAN**
┣👤 **User:** {user}
┣🆔 **ID:** `{user_id}`
┣🔨 **Status:** `Globally Hammered`
┗━━━━━━━⚔️━━━━━━━┛
"""

    MUTE_TXT = """
┏━🔇 **ACTION: MUTE**
┣👤 **User:** {user}
┣⏳ **Duration:** `{duration}`
┣📜 **Reason:** `Restricted access`
┗━━━━━━━📵━━━━━━━┛
"""
