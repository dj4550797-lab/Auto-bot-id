class Script(object):
    START_TXT = """
┏━━📦 **FLIXORA ID BOT**
┃
┣👤 **Hello** {first_name}
┣🤖 **Status:** `Operational` 🟢
┃
┣📜 **I am a specialized ID Tool.**
┃ I can fetch User, Group, Channel,
┃ and Sticker IDs instantly.
┃
┣⚡ **Library:** `Pyrogram`
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    HELP_TXT = """
┏━━🛠️ **COMMAND MENU**
┃
┣🔹 `/id` - Get Chat & User ID
┃ (Reply to someone for their ID)
┃
┣🔹 `/stickerid` - Get Sticker info
┃ (Reply to any sticker)
┃
┣🔹 `/info` - Advanced User info
┃
┣📡 **Channels:** Reply to a 
┃ forwarded msg to get Channel ID.
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    ID_TXT = """
┏━━🆔 **IDENTITY INFO**
┃
┣🔹 **Chat ID:** `{chat_id}`
┣👤 **User ID:** `{user_id}`
┃
┣🎯 **Replied:** `{replied_id}`
┣📢 **Forward:** `{forward_id}`
┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""
