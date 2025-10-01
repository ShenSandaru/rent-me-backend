from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId


class GeoPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class LocationModel(BaseModel):
    id: Optional[str] = None
    name: str
    address: str
    coordinates: GeoPoint
    city: str
    state: str
    country: str
    postal_code: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

class RentalBase(BaseModel):
    name: str
    address: str
    description: Optional[str] = None
    location: GeoPoint

class RentalCreate(RentalBase):
    pass  # For creating new rentals

class Rental(RentalBase):
    id: str  # MongoDB _id as string

class NearbySearch(BaseModel):  # Response model for search
    rentals: List[Rental]