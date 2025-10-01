from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.item import ItemModel, ItemCreateModel, NearbyItemsResponse
from ..models.user import PyObjectId
from typing import List, Optional
from datetime import datetime
import re

async def get_all_items(db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Retrieves all items from the database."""
    try:
        items_cursor = db.get_collection("items").find({"status": "available"})
        items = await items_cursor.to_list(length=100)
        return [ItemModel(**item) for item in items]
    except Exception as e:
        print(f"⚠️  Database error in get_all_items: {e}")
        return []

async def create_new_item(item_data: ItemCreateModel, db: AsyncIOMotorDatabase, owner_id: PyObjectId) -> ItemModel:
    """Creates a new item in the database with location data."""
    try:
        # Convert item data to dict using Pydantic v2 model_dump
        item_dict = item_data.model_dump()
        
        # Add metadata
        item_dict["ownerId"] = owner_id
        item_dict["createdAt"] = datetime.utcnow()
        item_dict["updatedAt"] = datetime.utcnow()
        
        # Create GeoJSON location for MongoDB spatial queries
        item_dict["geoLocation"] = item_data.location.to_geo_point()
        
        # Insert into database
        result = await db.get_collection("items").insert_one(item_dict)
        
        # Retrieve the created item
        created_item = await db.get_collection("items").find_one({"_id": result.inserted_id})
        
        return ItemModel(**created_item)
    except Exception as e:
        print(f"⚠️  Database error in create_new_item: {e}")
        raise

async def find_nearby_items(
    latitude: float, 
    longitude: float, 
    radius_km: int, 
    db: AsyncIOMotorDatabase,
    category: Optional[str] = None
) -> NearbyItemsResponse:
    """Find items near the specified coordinates within the given radius."""
    try:
        # MongoDB requires a 2dsphere index for $near queries.
        # Ensure it's created at startup.
        query = {
            "geoLocation": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "$maxDistance": radius_km * 1000  # Convert km to meters
                }
            },
            "status": "available"
        }
        
        if category:
            query["category"] = category
            
        cursor = db.get_collection("items").find(query)
        items_data = await cursor.to_list(length=50)
        
        return NearbyItemsResponse(
            items=[ItemModel(**item) for item in items_data],
            center={"latitude": latitude, "longitude": longitude},
            radius=radius_km * 1000
        )
    except Exception as e:
        print(f"⚠️  Database error in find_nearby_items: {e}")
        raise

async def get_items_by_category(category: str, db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Get items filtered by category."""
    try:
        query = {"category": re.compile(f"^{category}$", re.IGNORECASE), "status": "available"}
        cursor = db.get_collection("items").find(query)
        items_data = await cursor.to_list(length=50)
        return [ItemModel(**item) for item in items_data]
    except Exception as e:
        print(f"⚠️  Database error in get_items_by_category: {e}")
        return []

async def search_items_by_text(q: str, category: Optional[str], db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Search for items by text in title and description."""
    try:
        # Using regex for a simple text search. For production, consider a text index.
        search_regex = re.compile(q, re.IGNORECASE)
        query = {
            "$or": [{"title": search_regex}, {"description": search_regex}],
            "status": "available"
        }
        if category:
            query["category"] = category

        cursor = db.get_collection("items").find(query)
        items_data = await cursor.to_list(length=50)
        return [ItemModel(**item) for item in items_data]
    except Exception as e:
        print(f"⚠️  Database error in search_items_by_text: {e}")
        return []

async def create_geo_index_for_items(db: AsyncIOMotorDatabase):
    """Create 2dsphere index for geoLocation field in items collection. Call this at startup."""
    try:
        await db.get_collection("items").create_index([("geoLocation", "2dsphere")])
        print("✅ Geo index created for 'items' collection.")
    except Exception as e:
        print(f"⚠️  Could not create geo index for 'items': {e}")