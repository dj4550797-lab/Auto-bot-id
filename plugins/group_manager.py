from pyrogram import Client, filters
from pyrogram.types import Message

# --- 1. WELCOME SYSTEM (ROSE BOT LIKE) ---
@Client.on_message(filters.new_chat_members)
async def welcome_new_members(client, message: Message):
    for member in message.new_chat_members:
        # Agar bot khud group mein add hua hai
        if member.is_self:
            await message.reply_text(
                "**Thank you for adding me to this group! 🥳**\n"
                "Main group manage karne aur IDs find karne mein aapki madad karunga.\n"
                "Check my features using /help."
            )
        # Agar koi naya user aaya hai
        else:
            await message.reply_text(
                f"**Welcome {member.mention} to {message.chat.title}! 🎉**\n"
                f"Umeed hai aapko yahan achha lagega."
            )

# --- 2. LEAVE SYSTEM ---
@Client.on_message(filters.left_chat_member)
async def goodbye_members(client, message: Message):
    if message.left_chat_member.is_self:
        return # Agar bot khud left hua to kuch mat karo
    
    await message.reply_text(
        f"**Goodbye {message.left_chat_member.first_name} 😢**\n"
        f"Aapse milkar achha laga."
    )

# --- 3. AUTO-REACTION SYSTEM ---
@Client.on_message(filters.text & filters.group, group=1)
async def auto_reaction(client, message: Message):
    text = message.text.lower()
    
    # Keyword based auto-reactions
    try:
        if "hello" in text or "hi" in text or "hey" in text:
            await message.react("👋")
        elif "awesome" in text or "wow" in text:
            await message.react("🤩")
        elif "bot" in text:
            await message.react("🤖")
        elif "thanks" in text or "thank you" in text:
            await message.react("❤️")
    except Exception:
        # Ignore if bot doesn't have reaction permissions in that group
        pass
