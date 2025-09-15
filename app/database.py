from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Create the MongoDB client and database instances
client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
db = client.get_database("rent_me")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for handling the lifespan of a FastAPI application.
    It connects to the MongoDB database on startup and closes the connection on shutdown.
    """
    # The connection is already established, just yield
    print("Successfully connected to MongoDB.")
    
    yield
    
    # Close the MongoDB connection
    client.close()
    print("MongoDB connection closed.")

def get_database() -> AsyncIOMotorDatabase:
    """Returns the database instance."""
    return db
