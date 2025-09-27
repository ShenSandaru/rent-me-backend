from fastapi import APIRouter, Depends, Query, HTTPException
from ..database import get_database
from ..models.item import ItemModel, ItemCreateModel, NearbyItemsResponse
from ..models.user import UserInDB
from typing import List, Optional
from ..services import item_service
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..dependencies import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[ItemModel])
async def get_all_items(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get all available rental items."""
    return await item_service.get_all_items(db)

@router.post("/", response_model=ItemModel)
async def create_item(
    item: ItemCreateModel, 
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: UserInDB = Depends(get_current_user)
):
    """Create a new rental item (requires authentication)."""
    try:
        # Get owner ID from current user (UserInDB has email attribute)
        owner_id = current_user.email
        return await item_service.create_new_item(item, db, owner_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nearby", response_model=NearbyItemsResponse)
async def get_nearby_items(
    latitude: float = Query(..., description="Latitude of search center"),
    longitude: float = Query(..., description="Longitude of search center"),
    radius: int = Query(5, description="Search radius in kilometers", ge=1, le=50),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Find rental items near the specified coordinates within the given radius.
    This is the main endpoint for map-based item search.
    """
    try:
        return await item_service.find_nearby_items(latitude, longitude, radius, db, category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/category/{category}", response_model=List[ItemModel])
async def get_items_by_category(
    category: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get items filtered by category."""
    try:
        return await item_service.get_items_by_category(category, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search", response_model=List[ItemModel])
async def search_items(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Search items by title or description."""
    # This could be enhanced with text search capabilities
    return await item_service.get_all_items(db)