from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .user import PyObjectId # Import PyObjectId

class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    description: str
    price_per_day: float
    availability: bool = True
    owner_id: PyObjectId # Use PyObjectId
    images: List[str] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class ItemCreateSchema(BaseModel):
    name: str
    description: str
    price_per_day: float
    images: List[str] = []

class ItemUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_day: Optional[float] = None
    availability: Optional[bool] = None
    images: Optional[List[str]] = None