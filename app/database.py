from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
db: AsyncIOMotorDatabase = client.get_database("rent_me")

# Collections
UsersCollection = db.get_collection("users")
OwnersCollection = db.get_collection("owners")
ItemsCollection = db.get_collection("items")
ChatsCollection = db.get_collection("chats")
RentalsCollection = db.get_collection("rentals")
PaymentsCollection = db.get_collection("payments")
