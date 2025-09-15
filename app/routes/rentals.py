from fastapi import APIRouter, Depends
from ..database import get_database
from ..models.rental import RentalModel
from typing import List
from ..services import rental_service
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.get("/", response_model=List[RentalModel])
async def get_rentals(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await rental_service.get_all_rentals(db)

@router.post("/", response_model=RentalModel)
async def create_rental(rental: RentalModel, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await rental_service.create_new_rental(rental, db)