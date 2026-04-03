from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URI, DB_NAME

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        
        # All Collections
        self.banned_users, self.groups = self.db.banned_users, self.db.groups
        self.welcomes, self.warns = self.db.welcomes, self.db.warns
        self.filters, self.notes, self.rules = self.db.filters, self.db.notes, self.db.rules
        self.locks, self.approvals = self.db.locks, self.db.approvals
        self.blocklists, self.settings = self.db.blocklists, self.db.settings
        self.federations, self.fed_subs = self.db.federations, self.db.fed_subs
        self.disabled_cmds = self.db.disabled_cmds
        self.log_channels = self.db.log_channels

    # --- CORE ---
    async def ban_user(self, user_id): await self.banned_users.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)
    async def unban_user(self, user_id): await self.banned_users.delete_one({"_id": user_id})
    async def is_banned(self, user_id): return bool(await self.banned_users.find_one({"_id": user_id}))
    async def add_group(self, chat_id, title): await self.groups.update_one({"_id": chat_id}, {"$set": {"title": title}}, upsert=True)
    async def get_all_groups(self): return await self.groups.find({}).to_list(length=None)

    # --- SETTINGS, WELCOME, RULES ---
    async def set_setting(self, chat_id, key, value): await self.settings.update_one({"_id": chat_id}, {"$set": {key: value}}, upsert=True)
    async def get_setting(self, chat_id, key): res = await self.settings.find_one({"_id": chat_id}); return res.get(key) if res else None
    async def set_welcome(self, chat_id, text): await self.welcomes.update_one({"_id": chat_id}, {"$set": {"text": text}}, upsert=True)
    async def get_welcome(self, chat_id): res = await self.welcomes.find_one({"_id": chat_id}); return res.get("text") if res else None
    async def set_rules(self, chat_id, rules): await self.rules.update_one({"_id": chat_id}, {"$set": {"rules": rules}}, upsert=True)
    async def get_rules(self, chat_id): res = await self.rules.find_one({"_id": chat_id}); return res.get("rules") if res else None

    # --- FILTERS, NOTES, LOCKS, APPROVALS, BLOCKLISTS ---
    async def add_filter(self, chat_id, word, reply): await self.filters.update_one({"chat_id": chat_id, "word": word}, {"$set": {"reply": reply}}, upsert=True)
    async def get_filters(self, chat_id): return await self.filters.find({"chat_id": chat_id}).to_list(length=None)
    async def save_note(self, chat_id, name, text): await self.notes.update_one({"chat_id": chat_id, "name": name}, {"$set": {"text": text}}, upsert=True)
    async def get_note(self, chat_id, name): res = await self.notes.find_one({"chat_id": chat_id, "name": name}); return res.get("text") if res else None
    async def update_lock(self, chat_id, lock_type, status): await self.locks.update_one({"_id": chat_id}, {"$set": {lock_type: status}}, upsert=True)
    async def get_locks(self, chat_id): return await self.locks.find_one({"_id": chat_id}) or {}
    async def approve_user(self, chat_id, user_id): await self.approvals.update_one({"_id": f"{chat_id}_{user_id}"}, {"$set": {}}, upsert=True)
    async def is_approved(self, chat_id, user_id): return bool(await self.approvals.find_one({"_id": f"{chat_id}_{user_id}"}))
    async def add_blocklist(self, chat_id, word): await self.blocklists.update_one({"chat_id": chat_id, "word": word}, {"$set": {}}, upsert=True)
    async def get_blocklist(self, chat_id): return [x["word"] for x in await self.blocklists.find({"chat_id": chat_id}).to_list(length=None)]

    # --- NEW: LOG CHANNELS & DISABLING ---
    async def set_log_channel(self, chat_id, log_channel_id): await self.log_channels.update_one({"_id": chat_id}, {"$set": {"log_channel": log_channel_id}}, upsert=True)
    async def get_log_channel(self, chat_id): res = await self.log_channels.find_one({"_id": chat_id}); return res.get("log_channel") if res else None
    async def disable_command(self, chat_id, cmd): await self.disabled_cmds.update_one({"chat_id": chat_id, "cmd": cmd}, {"$set": {}}, upsert=True)
    async def enable_command(self, chat_id, cmd): await self.disabled_cmds.delete_one({"chat_id": chat_id, "cmd": cmd})
    async def is_disabled(self, chat_id, cmd): return bool(await self.disabled_cmds.find_one({"chat_id": chat_id, "cmd": cmd}))
    
db = Database(MONGO_URI, DB_NAME)