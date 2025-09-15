from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import auth, users
from app.config import settings
from app.database import connect_to_database, close_database_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to the database on startup and disconnect on shutdown."""
    await connect_to_database(uri=settings.MONGO_DATABASE_URI, db_name="rent-me")
    yield
    await close_database_connection()

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0",
    lifespan=lifespan
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)