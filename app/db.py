# app/db.py
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pydantic import BaseModel
from app.config import settings
from anyio import to_thread

client: MongoClient | None = None
_db: Database | None = None   # underscore to discourage direct imports


def _ensure_indexes(database: Database) -> None:
    database.organizations.create_index("name", unique=True)
    database.users.create_index([("org_id", ASCENDING), ("id", ASCENDING)], unique=True)
    database.users.create_index([("org_id", ASCENDING), ("email", ASCENDING)], unique=True)
    database.notes.create_index([("org_id", ASCENDING), ("id", ASCENDING)], unique=True)
    database.notes.create_index([("org_id", ASCENDING)])


async def connect_to_mongo():
    global client, _db
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    await to_thread.run_sync(lambda: client.admin.command("ping"))
    _db = client["notes_multi_tenant"]
    await to_thread.run_sync(lambda: _ensure_indexes(_db))
    print("✓ MongoDB connected successfully")


async def close_mongo_connection():
    global client, _db
    if client:
        client.close()
    client = None
    _db = None


async def ensure_db() -> Database:
    global client, _db
    if _db is not None:
        return _db
    # Lazy init (same logic as startup)
    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    await to_thread.run_sync(lambda: client.admin.command("ping"))
    _db = client[settings.DB_NAME]
    await to_thread.run_sync(lambda: _ensure_indexes(_db))
    return _db
