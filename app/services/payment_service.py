from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.payment import PaymentModel
from typing import List

async def get_all_payments(db: AsyncIOMotorDatabase) -> List[PaymentModel]:
    """Retrieves all payments from the database."""
    payments_cursor = db.get_collection("payments").find()
    payments = await payments_cursor.to_list(length=100)
    return [PaymentModel(**payment) for payment in payments]

async def create_new_payment(payment_data: PaymentModel, db: AsyncIOMotorDatabase) -> PaymentModel:
    """Creates a new payment in the database."""
    payment_dict = payment_data.dict(by_alias=True, exclude={"id"})
    result = await db.get_collection("payments").insert_one(payment_dict)
    created_payment = await db.get_collection("payments").find_one({"_id": result.inserted_id})
    return PaymentModel(**created_payment)