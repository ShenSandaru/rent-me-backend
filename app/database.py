import motor.motor_asyncio
from .config import settings

class DataBase:
    client: motor.motor_asyncio.AsyncIOMotorClient = None

db = DataBase()

async def get_database_client() -> motor.motor_asyncio.AsyncIOMotorClient:
    """Returns the database client instance."""
    return db.client

async def connect_to_mongo():
    """Connects to the MongoDB database."""
    print("Connecting to MongoDB...")
    db.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    print("Connected to MongoDB.")

async def close_mongo_connection():
    """Closes the MongoDB database connection."""
    print("Closing MongoDB connection...")
    db.client.close()
    print("Closed MongoDB connection.")

# You can no longer define collections here. They must be accessed via the client.