from bson import ObjectId
from pymongo.errors import PyMongoError
from ..database import get_db
from ..models.location import Rental, RentalCreate, GeoPoint

db = get_db()
collection = db.rentals  # Collection for rentals

# Create 2dsphere index if not exists (run once, e.g., in main.py startup)
def create_geo_index():
    collection.create_index([("location", "2dsphere")])

# Create a new rental location
def create_rental(rental: RentalCreate) -> Rental:
    rental_dict = rental.model_dump()
    result = collection.insert_one(rental_dict)
    return Rental(id=str(result.inserted_id), **rental_dict)

# Find nearby rentals
def find_nearby(lat: float, lon: float, max_distance_meters: int = 5000) -> list[Rental]:
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
        results = collection.find(query)
        return [Rental(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}) for doc in results]
    except PyMongoError as e:
        raise ValueError(f"Database error: {str(e)}")

# Get all rental locations
def get_all_rentals() -> list[Rental]:
    try:
        results = collection.find()
        return [Rental(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}) for doc in results]
    except PyMongoError as e:
        raise ValueError(f"Database error: {str(e)}")