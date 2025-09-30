from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum
from .user import PyObjectId # Import PyObjectId

class RentalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RentalModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    item_id: PyObjectId # Use PyObjectId
    renter_id: PyObjectId # Use PyObjectId
    owner_id: PyObjectId # Use PyObjectId
    start_date: datetime
    end_date: datetime
    total_price: float
    status: RentalStatus = RentalStatus.PENDING
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class RentalCreateSchema(BaseModel):
    item_id: PyObjectId # Use PyObjectId
    start_date: datetime
    end_date: datetime

class RentalUpdateSchema(BaseModel):
    status: RentalStatus