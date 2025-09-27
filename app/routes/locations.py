from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ..services.location_service import create_rental, find_nearby, get_all_rentals
from ..models.location import Rental, RentalCreate, NearbySearch
from ..dependencies import get_current_user

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/", response_model=Rental)
async def create_rental_location(
    rental_data: RentalCreate, 
    current_user=Depends(get_current_user)
):
    """
    Create a new rental location with geographic coordinates.
    Requires authentication.
    """
    try:
        return create_rental(rental_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nearby", response_model=NearbySearch)
async def get_nearby_rentals(
    latitude: float = Query(..., description="Latitude of search center"),
    longitude: float = Query(..., description="Longitude of search center"),
    radius: int = Query(5, description="Search radius in kilometers", ge=1, le=100)
):
    """
    Find rental locations near the specified coordinates within the given radius.
    Public endpoint - no authentication required.
    """
    try:
        rentals = find_nearby(latitude, longitude, radius * 1000)  # Convert km to meters
        return NearbySearch(rentals=rentals)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Rental])
async def get_all_rental_locations():
    """
    Get all available rental locations.
    Public endpoint - no authentication required.
    """
    try:
        return get_all_rentals()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))