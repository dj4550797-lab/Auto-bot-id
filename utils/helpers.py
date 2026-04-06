async def is_group_admin(client, message, chat_id: int = None) -> bool:
    target_chat_id = chat_id or message.chat.id
    if message.chat.type.name == "PRIVATE" and not chat_id: return False
    
    # If anonymous admin or channel message
    if not message.from_user:
        if message.sender_chat and message.sender_chat.id == target_chat_id:
            return True
        return False

    try:
        member = await client.get_chat_member(target_chat_id, message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False
