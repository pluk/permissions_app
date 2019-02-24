import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


class PermissionsService:
    def __init__(self):
        self.db = AsyncIOMotorClient('mongo', 27017, username='root', password='example').app

    async def get_permission(self, app_id, hl):
        return await self.db.permissions.\
            find_one({'appId': app_id, 'hl': hl})

    async def add_query(self, app_id, hl):
        data = {'appId': app_id, 'hl': hl}

        result = await self.db.permission_queries.\
            update_one(filter=data, update={'$setOnInsert': data}, upsert=True)

        print(result)