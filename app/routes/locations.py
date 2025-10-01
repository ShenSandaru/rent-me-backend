from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from ..import services
from ..database import get_database
from ..services.location_service import create_rental, find_nearby, get_all_rentals
from ..models.location import Rental, RentalCreate, NearbySearch
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/locations", 
    tags=["Locations"]
)

@router.post("/", response_model=Rental)
async def create_rental_location(
    rental_data: RentalCreate, 
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)  # This line requires authentication
):
    """
    Create a new rental location with geographic coordinates.
    Requires authentication.
    """
    try:
        return await create_rental(db, rental_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/nearby", response_model=NearbySearch)
async def get_nearby_rentals(
    latitude: float = Query(..., description="Latitude of search center"),
    longitude: float = Query(..., description="Longitude of search center"),
    radius: int = Query(5, description="Search radius in kilometers", ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Find rental locations near the specified coordinates within the given radius.
    Public endpoint - no authentication required.
    """

    try:        
        rentals = await find_nearby(db, latitude, longitude, radius * 1000)  # Convert km to meters
        return NearbySearch(rentals=rentals)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/", response_model=List[Rental])
async def get_all_rental_locations(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get all available rental locations.
    Public endpoint - no authentication required.
    """
    try:
        return await get_all_rentals(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))