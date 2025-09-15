from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI

class DataBase:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_connection = DataBase()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for handling the lifespan of a FastAPI application.
    It connects to the MongoDB database on startup and closes the connection on shutdown.
    """
    # Connect to MongoDB
    db_connection.client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    db_connection.db = db_connection.client.get_database("rent_me")
    print("Successfully connected to MongoDB.")
    
    yield
    
    # Close the MongoDB connection
    db_connection.client.close()
    print("MongoDB connection closed.")

def get_database() -> AsyncIOMotorDatabase:
    """Returns the database instance."""
    return db_connection.db
