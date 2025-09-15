from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.payment import PaymentModel
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PaymentModel])
async def get_payments():
    payments = await db.Payments.find().to_list(100)
    return payments

@router.post("/", response_model=PaymentModel)
async def create_payment(payment: PaymentModel):
    payment_dict = payment.dict(by_alias=True)
    if payment_dict.get("_id") is None:
        payment_dict.pop("_id", None)
    result = await db.Payments.insert_one(payment_dict)
    payment_dict["_id"] = result.inserted_id
    return payment_dict