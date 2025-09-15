from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.item import ItemModel
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ItemModel])
async def get_items():
    items = await db.Items.find().to_list(100)
    return items

@router.post("/", response_model=ItemModel)
async def create_item(item: ItemModel):
    item_dict = item.dict(by_alias=True)
    # Remove _id if it's None so MongoDB can auto-generate it
    if item_dict.get("_id") is None:
        item_dict.pop("_id", None)
    result = await db.Items.insert_one(item_dict)
    item_dict["_id"] = result.inserted_id
    return item_dict