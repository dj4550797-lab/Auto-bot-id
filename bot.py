import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand

# --- Fetch credentials from Render Environment Variables ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("FlixoraIDBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- COMMAND: /start & /help ---
@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message):
    text = (
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        f"I am an advanced ID Bot. Click the **Menu** button below to see what I can do!\n\n"
        f"🔹 `/id` - Get your ID and Chat ID.\n"
        f"🔹 Reply to a user with `/id` to get their ID.\n"
        f"🔹 Reply to a forwarded message with `/id` to get the Channel ID.\n"
        f"🔹 Reply to a sticker with `/stickerid` to get the Sticker ID."
    )
    await message.reply_text(text, quote=True)

# --- COMMAND: /id ---
@app.on_message(filters.command("id"))
async def id_command(client, message):
    text = f"**📌 Current Chat ID:** `{message.chat.id}`\n"
    
    if message.from_user:
        text += f"**👤 Your User ID:** `{message.from_user.id}`\n"
    
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        if replied_user:
            text += f"**🎯 Replied User ID:** `{replied_user.id}`\n"
        
        # Check if the message was forwarded from a channel/user
        if message.reply_to_message.forward_from:
            text += f"**↪️ Forwarded User ID:** `{message.reply_to_message.forward_from.id}`\n"
        elif message.reply_to_message.forward_from_chat:
            text += f"**📢 Forwarded Channel ID:** `{message.reply_to_message.forward_from_chat.id}`\n"
            
    await message.reply_text(text, quote=True)

# --- COMMAND: /stickerid ---
@app.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id_command(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker = message.reply_to_message.sticker
        text = (
            f"**🎟 Sticker Info**\n\n"
            f"**File ID:**\n`{sticker.file_id}`\n\n"
            f"**Unique ID:**\n`{sticker.file_unique_id}`"
        )
        await message.reply_text(text, quote=True)
    else:
        await message.reply_text("⚠️ **Please reply to a sticker with this command!**", quote=True)

# --- MAIN STARTUP & MENU CONFIGURATION ---
async def main():
    print("Starting bot...")
    await app.start()
    
    # This creates the Menu Button automatically!
    await app.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("id", "Get User, Group, or Channel ID"),
        BotCommand("stickerid", "Get Sticker File ID"),
        BotCommand("help", "How to use this bot")
    ])
    print("Menu button set successfully! Bot is now running.")
    
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())