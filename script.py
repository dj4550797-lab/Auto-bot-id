class Script(object):
    START_TXT = """
┏━━📦 **FLIXORA ID HUB**
┃
┣👤 **Hello** {first_name}
┣🤖 **Status:** `Active` 🟢
┃
┣📜 **Instructions:**
┃ ID dhoondhne ke liye `/how` type karein.
┃ Specific ID ke liye message ko reply karein.
┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    HOW_TO_TXT = """
┏━━❓ **HOW TO FIND IDs?**
┃
┣👤 **User ID:**
┃ Kisi bhi user ke message ko
┃ reply karke `/id` likhein.
┃
┣📢 **Channel ID:**
┃ Channel ka message bot ko
┃ **Forward** karein aur uspar
┃ `/id` likh kar reply karein.
┃
┣👥 **Group ID:**
┃ Group mein bas `/id` likhein.
┃
┣🎫 **Sticker ID:**
┃ Sticker par reply karke `/stid` likhein.
┃
┣🔄 **Sticker from ID:**
┃ `/getsticker [file_id]` type karein.
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    GUIDE_BTN = [
        ["❓ ID Kaise Dhundhein?", "how_to_use"]
    ]
