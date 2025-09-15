import motor.motor_asyncio
from .config import settings

# Create a client to connect to your MongoDB instance
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)

# Get the database (it will be created if it doesn't exist)
db = client.get_database("rent_me")

# Get a collection for users (it will be created if it doesn't exist)
UserCollection = db.get_collection("Users")