# This file is intentionally left empty.
# The database connection is now managed entirely within app/dependencies.py
# to ensure compatibility with serverless environments.

import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
db = client.get_database("rent_me")

# Define separate collections for Users and Owners
UsersCollection = db.get_collection("users")
OwnersCollection = db.get_collection("owners")

# Define collections for items, chats, payments, and rentals
ItemCollection = db.get_collection("items")
ChatsCollection = db.get_collection("chats")
PaymentsCollection = db.get_collection("payments")
RentalsCollection = db.get_collection("rentals")