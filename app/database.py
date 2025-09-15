import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# A singleton-like class to hold our database state
class MongoManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_manager = MongoManager()

async def connect_to_database(uri: str, db_name: str):
    """Initializes the database connection and stores it in the manager."""
    print("Connecting to MongoDB...")
    db_manager.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db_manager.db = db_manager.client.get_database(db_name)
    print("Connected to MongoDB.")

async def close_database_connection():
    """Closes the database connection."""
    print("Closing MongoDB connection...")
    if db_manager.client:
        db_manager.client.close()
    print("Closed MongoDB connection.")

def get_database() -> AsyncIOMotorDatabase:
    """A dependency function to return the database object from the manager."""
    return db_manager.db