from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from .user import PyObjectId
from .location import LocationModel, GeoPoint

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
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    ownerId: PyObjectId
    title: str
    description: str
    category: str
    pricePerHour: float
    pricePerDay: float
    location: LocationModel
    geoLocation: Optional[GeoPoint] = None  # GeoJSON for MongoDB spatial queries
    status: str
    images: List[str]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class ItemUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    pricePerHour: Optional[float] = None
    pricePerDay: Optional[float] = None
    location: Optional[LocationModel] = None
    status: Optional[str] = None
    images: Optional[List[str]] = None
        
class ItemSearchResponse(BaseModel):
    items: List[ItemModel]
    total: int
    
class NearbyItemsResponse(BaseModel):
    items: List[ItemModel]
    center: dict  # The search center coordinates
    radius: int   # Search radius in meters