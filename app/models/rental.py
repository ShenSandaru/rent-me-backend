from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class RentalModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    itemId: PyObjectId
    renterId: PyObjectId
    ownerId: PyObjectId
    qrCode: str
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    status: str
    totalAmount: int
    paymentStatus: str
    createdAt: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True