from fastapi import FastAPI
from app.routes import auth, users, items, chats, rentals, payments, locations
from app.services.location_service import create_geo_index
from app.services.item_service import create_geo_index_for_items
from app.database import get_db

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0"
)

# On startup - create geo indexes for location searches
@app.on_event("startup")
async def startup_event():
    try:
        create_geo_index()  # Ensure geo index exists for location queries
        print("✅ Geo index created successfully for locations")
    except Exception as e:
        print(f"⚠️  Warning: Could not create geo index for locations: {e}")
    
    try:
        # Create geo index for items collection
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.config import settings
        client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
        db = client.get_database(settings.DATABASE_NAME)
        await create_geo_index_for_items(db)
    except Exception as e:
        print(f"⚠️  Warning: Could not create geo index for items: {e}")
        print("📝 Note: Location-based item search will still work, but may be slower")

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chats.router)
app.include_router(rentals.router)
app.include_router(payments.router)
app.include_router(locations.router)