from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URI, DB_NAME

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.banned_users = self.db.banned_users
        self.groups = self.db.groups

    # --- BAN / UNBAN USERS ---
    async def ban_user(self, user_id):
        await self.banned_users.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)

    async def unban_user(self, user_id):
        await self.banned_users.delete_one({"_id": user_id})

    async def is_banned(self, user_id):
        user = await self.banned_users.find_one({"_id": user_id})
        return bool(user)

    # --- GROUP TRACKING ---
    async def add_group(self, chat_id, title):
        await self.groups.update_one({"_id": chat_id}, {"$set": {"title": title}}, upsert=True)

    async def remove_group(self, chat_id):
        await self.groups.delete_one({"_id": chat_id})

    async def get_all_groups(self):
        return await self.groups.find({}).to_list(length=None)

# Initialize Database
db = Database(MONGO_URI, DB_NAME)
