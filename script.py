class Script(object):

    # --- START MESSAGE ---
    START_TXT = """
👋 **Hello {first_name}!**

I am an **Advanced Telegram ID & Info Bot** 🤖.
I can help you extract detailed information about Users, Groups, Channels, and Stickers, including **Premium Status** and **Unique IDs**.

**Features:**
✅ Check User ID & Premium Status.
✅ Check Group & Channel IDs.
✅ Extract Sticker `file_id` and `unique_id`.
✅ Real-time System Uptime & Live Status.

Hit the **Help** button or type `/help` to see all available commands!
"""

    # --- HELP MESSAGE ---
    HELP_TXT = """
🛠 **Available Commands & Usage:**

**👤 User Commands:**
🔹 `/id` - Get your ID, Chat ID, and Premium status.
🔹 `/id` (reply to user) - Get the Replied User's ID and Premium status.
🔹 `/id` (reply to forwarded message) - Get the original Channel/User ID.
🔹 `/stickerid` (reply to sticker) - Get the sticker's File ID, Unique ID, and Premium status.
🔹 `/alive` - Check if the bot is online, plus CPU, RAM, and Uptime stats.

**👑 Admin Commands:**
🔸 `/ban [reply to user]` - Ban a user from using the bot.
🔸 `/unban [reply to user]` - Unban a user.
🔸 `/groups` - Get a list of all groups the bot is currently in.

**💡 Pro Tip:** 
Add me to your group, and I will automatically log the group details (Members count, Group ID) to the Admin's Log Channel!
"""

    # --- ABOUT MESSAGE ---
    ABOUT_TXT = """
🤖 **About This Bot:**

📝 **Language:** [Python 3](https://www.python.org)
📚 **Library:** [Pyrogram](https://docs.pyrogram.org/)
🗄 **Database:** [MongoDB](https://www.mongodb.com/)
⚙️ **Server Stats:** Monitored via `psutil`
🛡 **Features:** Premium Check, Auto-Logs, Banning System.

*Created for advanced Telegram scraping and ID extraction.*
"""

    # --- ALIVE MESSAGE TEMPLATE ---
    ALIVE_TXT = """
🟢 **System is Live and Online!**

**💻 Server Stats:**
 ├ **CPU Usage:** `{cpu}%`
 ├ **RAM Usage:** `{ram}%`
 └ **Uptime:** `{uptime}`

**Bot is running smoothly!** 🚀
"""

    # --- BANNED MESSAGE ---
    BANNED_TXT = """
🚫 **Access Denied!**

You have been banned by the Admin from using this bot. 
If you think this is a mistake, please contact the bot owner.
"""