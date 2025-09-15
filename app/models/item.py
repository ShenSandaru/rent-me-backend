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

class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    ownerId: PyObjectId
    title: str
    description: str
    category: str
    pricePerHour: int
    pricePerDay: int
    location: dict
    status: str
    images: List[str]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    # ...existing code...

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True