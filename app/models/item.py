from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class GeoPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class LocationModel(BaseModel):
    latitude: float
    longitude: float
    address: str
    city: Optional[str] = None
    country: Optional[str] = None
    
    def to_geo_point(self) -> dict:
        """Convert to MongoDB GeoJSON format"""
        return {
            "type": "Point",
            "coordinates": [self.longitude, self.latitude]
        }

class ItemCreateModel(BaseModel):
    title: str
    description: str
    category: str
    pricePerHour: float
    pricePerDay: float
    location: LocationModel
    status: str = "available"
    images: List[str] = []

class ItemModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    ownerId: Optional[str] = None
    title: str
    description: str
    category: str
    pricePerHour: float
    pricePerDay: float
    location: LocationModel
    geoLocation: Optional[dict] = None  # GeoJSON for MongoDB spatial queries
    status: str
    images: List[str]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
        
class ItemSearchResponse(BaseModel):
    items: List[ItemModel]
    total: int
    
class NearbyItemsResponse(BaseModel):
    items: List[ItemModel]
    center: dict  # The search center coordinates
    radius: int   # Search radius in meters