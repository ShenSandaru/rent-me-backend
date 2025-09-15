from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.rental import RentalModel
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/", response_model=List[RentalModel])
async def get_rentals():
    rentals = await db.Rentals.find().to_list(100)
    return rentals

@router.post("/", response_model=RentalModel)
async def create_rental(rental: RentalModel):
    rental_dict = rental.dict(by_alias=True)
    if rental_dict.get("_id") is None:
        rental_dict.pop("_id", None)
    result = await db.Rentals.insert_one(rental_dict)
    rental_dict["_id"] = result.inserted_id
    return rental_dict