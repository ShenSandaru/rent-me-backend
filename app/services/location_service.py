from bson import ObjectId
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.location import Rental, RentalCreate

# Create 2dsphere index if not exists
async def create_geo_index(db: AsyncIOMotorDatabase):
    await db.rentals.create_index([("location", "2dsphere")])

# Create a new rental location
async def create_rental(db: AsyncIOMotorDatabase, rental: RentalCreate) -> Rental:
    rental_dict = rental.model_dump()
    result = await db.rentals.insert_one(rental_dict)
    created_rental = await db.rentals.find_one({"_id": result.inserted_id})
    return Rental(**created_rental)

# Find nearby rentals
async def find_nearby(db: AsyncIOMotorDatabase, lat: float, lon: float, max_distance_meters: int = 5000) -> list[Rental]:
    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": max_distance_meters
            }
        }
    }
    try:
        rentals_cursor = db.rentals.find(query)
        return [Rental(**doc) async for doc in rentals_cursor]
    except PyMongoError as e:
        raise ValueError(f"Database error: {str(e)}")

# Get all rental locations
async def get_all_rentals(db: AsyncIOMotorDatabase) -> list[Rental]:
    try:
        rentals_cursor = db.rentals.find()
        return [Rental(**doc) async for doc in rentals_cursor]
    except PyMongoError as e:
        raise ValueError(f"Database error: {str(e)}")