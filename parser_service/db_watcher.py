#!/usr/bin/env python

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import time
from parser import GooglePlayParser


client = AsyncIOMotorClient('mongo', 27017, username='root', password='example')

db = client.app

parser = GooglePlayParser()

async def remove_query(app_id):
    await db.permission_queries.delete_one({'appId': app_id})

async def do_insert(app_id, hl, permissions):
    document = {'appId': app_id, 'hl': hl, 'permissions': permissions}
    result = await db.permissions.update_one(
        {'appId': app_id, 'hl': hl},{'$setOnInsert': document}, upsert=True
    )
    return result

async def do_find():
    async for document in db.permission_queries.find():
        permissions = await parser.get_permissions(document['appId'], document['hl'])
        await do_insert(document['appId'], document['hl'], permissions)

        await remove_query(document['appId'])


async def f():
    while True:
        await do_find()
        time.sleep(15)

loop = asyncio.get_event_loop()

loop.run_until_complete(f())
