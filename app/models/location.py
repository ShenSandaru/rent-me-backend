from pydantic import BaseModel
from typing import List, Optional

class GeoPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

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