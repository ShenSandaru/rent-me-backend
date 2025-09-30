from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum
from .user import PyObjectId # Import PyObjectId

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    rental_id: PyObjectId # Use PyObjectId
    payer_id: PyObjectId # Use PyObjectId
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    stripe_charge_id: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class PaymentCreateSchema(BaseModel):
    rental_id: PyObjectId # Use PyObjectId
    amount: float