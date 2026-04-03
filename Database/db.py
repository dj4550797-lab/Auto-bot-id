from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URI, DB_NAME

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.banned_users = self.db.banned_users
        self.groups = self.db.groups
        self.welcomes = self.db.welcomes
        self.warns = self.db.warns
        self.filters = self.db.filters
        self.notes = self.db.notes
        self.rules = self.db.rules
        self.locks = self.db.locks

    async def ban_user(self, user_id): await self.banned_users.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)
    async def unban_user(self, user_id): await self.banned_users.delete_one({"_id": user_id})
    async def is_banned(self, user_id): return bool(await self.banned_users.find_one({"_id": user_id}))
    async def add_group(self, chat_id, title): await self.groups.update_one({"_id": chat_id}, {"$set": {"title": title}}, upsert=True)
    async def remove_group(self, chat_id): await self.groups.delete_one({"_id": chat_id})
    async def get_all_groups(self): return await self.groups.find({}).to_list(length=None)
    async def set_welcome(self, chat_id, text): await self.welcomes.update_one({"_id": chat_id}, {"$set": {"text": text}}, upsert=True)
    async def get_welcome(self, chat_id): res = await self.welcomes.find_one({"_id": chat_id}); return res["text"] if res else None
    async def add_warn(self, chat_id, user_id):
        doc_id = f"{chat_id}_{user_id}"
        res = await self.warns.find_one({"_id": doc_id})
        warns = (res["warns"] + 1) if res else 1
        await self.warns.update_one({"_id": doc_id}, {"$set": {"warns": warns}}, upsert=True)
        return warns
    async def reset_warns(self, chat_id, user_id): await self.warns.delete_one({"_id": f"{chat_id}_{user_id}"})
    async def add_filter(self, chat_id, word, reply): await self.filters.update_one({"chat_id": chat_id, "word": word}, {"$set": {"reply": reply}}, upsert=True)
    async def remove_filter(self, chat_id, word): await self.filters.delete_one({"chat_id": chat_id, "word": word})
    async def get_filters(self, chat_id): return await self.filters.find({"chat_id": chat_id}).to_list(length=None)
    async def save_note(self, chat_id, name, text): await self.notes.update_one({"chat_id": chat_id, "name": name}, {"$set": {"text": text}}, upsert=True)
    async def get_note(self, chat_id, name): res = await self.notes.find_one({"chat_id": chat_id, "name": name}); return res["text"] if res else None
    async def delete_note(self, chat_id, name): await self.notes.delete_one({"chat_id": chat_id, "name": name})
    async def get_all_notes(self, chat_id): return await self.notes.find({"chat_id": chat_id}).to_list(length=None)
    async def set_rules(self, chat_id, rules): await self.rules.update_one({"_id": chat_id}, {"$set": {"rules": rules}}, upsert=True)
    async def get_rules(self, chat_id): res = await self.rules.find_one({"_id": chat_id}); return res["rules"] if res else None
    async def update_lock(self, chat_id, lock_type, status): await self.locks.update_one({"_id": chat_id}, {"$set": {lock_type: status}}, upsert=True)
    async def get_locks(self, chat_id): res = await self.locks.find_one({"_id": chat_id}); return res if res else {}

db = Database(MONGO_URI, DB_NAME)