from fastapi import FastAPI
from contextlib import asynccontextmanager
import motor.motor_asyncio
from app.routes import auth, users
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Connect to the database on startup and disconnect on shutdown.
    The database client is attached to the app state for access in dependencies.
    """
    print("Connecting to MongoDB...")
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    app.db = app.mongodb_client.get_database("rent-me")
    print("Connected to MongoDB.")
    
    yield
    
    print("Closing MongoDB connection...")
    app.mongodb_client.close()
    print("Closed MongoDB connection.")

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0",
    lifespan=lifespan
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)