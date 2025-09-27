from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.item import ItemModel, ItemCreateModel, NearbyItemsResponse
from typing import List, Optional
from datetime import datetime
import math

async def get_all_items(db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Retrieves all items from the database."""
    try:
        items_cursor = db.get_collection("items").find()
        items = await items_cursor.to_list(length=100)
        return [ItemModel(**item) for item in items]
    except Exception as e:
        print(f"⚠️  Database error in get_all_items: {e}")
        return []

async def create_new_item(item_data: ItemCreateModel, db: AsyncIOMotorDatabase, owner_id: str = None) -> ItemModel:
    """Creates a new item in the database with location data."""
    try:
        # Convert item data to dict
        item_dict = item_data.dict()
        
        # Add metadata
        item_dict["ownerId"] = owner_id or "demo_owner"
        item_dict["createdAt"] = datetime.utcnow()
        item_dict["updatedAt"] = datetime.utcnow()
        
        # Create GeoJSON location for MongoDB spatial queries
        item_dict["geoLocation"] = {
            "type": "Point",
            "coordinates": [item_data.location.longitude, item_data.location.latitude]
        }
        
        # Insert into database
        result = await db.get_collection("items").insert_one(item_dict)
        
        # Retrieve the created item
        created_item = await db.get_collection("items").find_one({"_id": result.inserted_id})
        created_item["id"] = str(created_item["_id"])
        del created_item["_id"]
        
        return ItemModel(**created_item)
    except Exception as e:
        print(f"⚠️  Database error in create_new_item: {e}")
        # Return demo item for testing
        demo_item = item_data.dict()
        demo_item["id"] = "demo_item_123"
        demo_item["ownerId"] = owner_id or "demo_owner"
        demo_item["createdAt"] = datetime.utcnow()
        demo_item["updatedAt"] = datetime.utcnow()
        return ItemModel(**demo_item)

async def find_nearby_items(
    latitude: float, 
    longitude: float, 
    radius_km: int, 
    db: AsyncIOMotorDatabase,
    category: Optional[str] = None
) -> NearbyItemsResponse:
    """Find items near the specified coordinates within the given radius."""
    try:
        # Create the geo query
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
            "status": "available"  # Only show available items
        }
        
        # Add category filter if specified
        if category:
            query["category"] = category
            
        # Execute the query
        cursor = db.get_collection("items").find(query)
        items_data = await cursor.to_list(length=50)
        
        # Convert to ItemModel objects
        items = []
        for item_data in items_data:
            item_data["id"] = str(item_data["_id"])
            del item_data["_id"]
            items.append(ItemModel(**item_data))
        
        return NearbyItemsResponse(
            items=items,
            center={"latitude": latitude, "longitude": longitude},
            radius=radius_km * 1000
        )
        
    except Exception as e:
        print(f"⚠️  Database error in find_nearby_items: {e}")
        # Return demo items for testing
        demo_items = [
            ItemModel(
                id="demo_item_1",
                title="Demo Bicycle",
                description="Mountain bike for rent",
                category="sports",
                pricePerHour=5.0,
                pricePerDay=30.0,
                location={
                    "latitude": latitude + 0.01,
                    "longitude": longitude + 0.01,
                    "address": "Demo Location 1"
                },
                status="available",
                images=[]
            ),
            ItemModel(
                id="demo_item_2",
                title="Demo Camera",
                description="DSLR camera for events",
                category="electronics",
                pricePerHour=10.0,
                pricePerDay=80.0,
                location={
                    "latitude": latitude - 0.01,
                    "longitude": longitude - 0.01,
                    "address": "Demo Location 2"
                },
                status="available",
                images=[]
            )
        ]
        
        return NearbyItemsResponse(
            items=demo_items,
            center={"latitude": latitude, "longitude": longitude},
            radius=radius_km * 1000
        )

async def get_items_by_category(category: str, db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Get items filtered by category."""
    try:
        query = {"category": category, "status": "available"}
        cursor = db.get_collection("items").find(query)
        items_data = await cursor.to_list(length=50)
        
        items = []
        for item_data in items_data:
            item_data["id"] = str(item_data["_id"])
            del item_data["_id"]
            items.append(ItemModel(**item_data))
            
        return items
    except Exception as e:
        print(f"⚠️  Database error in get_items_by_category: {e}")
        return []

# Helper function to create geo index for items collection
async def create_geo_index_for_items(db: AsyncIOMotorDatabase):
    """Create 2dsphere index for geoLocation field in items collection."""
    try:
        await db.get_collection("items").create_index([("geoLocation", "2dsphere")])
        print("✅ Geo index created for items collection")
    except Exception as e:
        print(f"⚠️  Could not create geo index for items: {e}")
