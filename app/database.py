from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings
from typing import AsyncGenerator
from pymongo import MongoClient

# Use settings consistently
client = MongoClient(settings.MONGO_DATABASE_URI)
db = client[settings.DATABASE_NAME]

# Function to get DB (for dependency injection if needed)
def get_db():
    return db

async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Dependency function to get a database connection for each request.
    Creates a new client for each request and closes it when the request is done.
    """
    client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    db = client.get_database(settings.DATABASE_NAME)
    try:
        yield db
    finally:
        client.close()
