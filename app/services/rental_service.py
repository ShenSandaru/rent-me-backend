from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.rental import RentalModel
from typing import List

async def get_all_rentals(db: AsyncIOMotorDatabase) -> List[RentalModel]:
    """Retrieves all rentals from the database."""
    rentals_cursor = db.get_collection("rentals").find()
    rentals = await rentals_cursor.to_list(length=100)
    return [RentalModel(**rental) for rental in rentals]

async def create_new_rental(rental_data: RentalModel, db: AsyncIOMotorDatabase) -> RentalModel:
    """Creates a new rental in the database."""
    rental_dict = rental_data.dict(by_alias=True, exclude={"id"})
    result = await db.get_collection("rentals").insert_one(rental_dict)
    created_rental = await db.get_collection("rentals").find_one({"_id": result.inserted_id})
    return RentalModel(**created_rental)