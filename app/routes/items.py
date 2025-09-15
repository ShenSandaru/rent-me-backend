from fastapi import APIRouter, Depends
from ..database import get_database
from ..models.item import ItemModel
from typing import List
from ..services import item_service
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[ItemModel])
async def get_items(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await item_service.get_all_items(db)

@router.post("/", response_model=ItemModel)
async def create_item(item: ItemModel, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await item_service.create_new_item(item, db)