import asyncio
from pyrogram import Client, filters
from info import ADMINS
from database.db import db

# Admin filter
admin_filter = filters.create(lambda _, __, m: m.from_user and m.from_user.id in ADMINS)

@Client.on_message(filters.command("broadcast") & admin_filter)
async def broadcast_message(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ **Reply to a message** to broadcast it to all groups.")

    groups = await db.get_all_groups()
    if not groups:
        return await message.reply_text("Bot is not in any groups yet.")

    msg = await message.reply_text(f"⏳ **Broadcasting to {len(groups)} groups...**")
    
    successful = 0
    failed = 0

    for grp in groups:
        try:
            await message.reply_to_message.copy(grp["_id"])
            successful += 1
            await asyncio.sleep(1) # Sleep to avoid Telegram Spam limits (FloodWait)
        except Exception as e:
            failed += 1
            # If the bot was kicked, remove the group from DB
            await db.remove_group(grp["_id"])

    await msg.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"📢 **Total Groups:** `{len(groups)}`\n"
        f"✅ **Successful:** `{successful}`\n"
        f"❌ **Failed (Bot Kicked):** `{failed}`"
    )