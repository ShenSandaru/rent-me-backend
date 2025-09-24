from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings
from typing import AsyncGenerator

async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Dependency function to get a database connection for each request.
    Creates a new client for each request and closes it when the request is done.
    """
    client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    db = client.get_database("rent_me")
    try:
        yield db
    finally:
        client.close()
