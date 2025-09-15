from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import auth, users
from app.database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Connects to the database on startup and closes the connection on shutdown.
    """
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0",
    lifespan=lifespan  # Use the new lifespan manager
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)