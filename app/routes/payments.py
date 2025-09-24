from fastapi import APIRouter, Depends
from ..database import get_database
from ..models.payment import PaymentModel
from typing import List
from ..services import payment_service
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=List[PaymentModel])
async def get_payments(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await payment_service.get_all_payments(db)

@router.post("/", response_model=PaymentModel)
async def create_payment(payment: PaymentModel, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await payment_service.create_new_payment(payment, db)