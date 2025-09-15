import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
db = client.get_database("rent_me")

# Define separate collections for Users and Owners
UsersCollection = db.get_collection("Users")
OwnersCollection = db.get_collection("Owners")

# You can also add the items collection here for the next step
ItemCollection = db.get_collection("items")