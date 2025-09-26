from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.location_service import create_rental, find_nearby
from app.models.location import Rental, RentalCreate
from app.dependencies import get_current_user  # Assuming your JWT dep

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=Rental)
def create_location(rental: RentalCreate, current_user=Depends(get_current_user)):
    # Requires auth to create
    return create_rental(rental)

@router.get("/near", response_model=list[Rental])
def get_nearby(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    max_distance: int = Query(5000, description="Max distance in meters")
):
    # Public endpoint for search (no auth needed, but you can add if wanted)
    try:
        return find_nearby(lat, lon, max_distance)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))