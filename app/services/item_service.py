from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.item import ItemModel
from typing import List

async def get_all_items(db: AsyncIOMotorDatabase) -> List[ItemModel]:
    """Retrieves all items from the database."""
    items_cursor = db.get_collection("items").find()
    items = await items_cursor.to_list(length=100)
    return [ItemModel(**item) for item in items]

async def create_new_item(item_data: ItemModel, db: AsyncIOMotorDatabase) -> ItemModel:
    """Creates a new item in the database."""
    item_dict = item_data.dict(by_alias=True, exclude={"id"})
    result = await db.get_collection("items").insert_one(item_dict)
    created_item = await db.get_collection("items").find_one({"_id": result.inserted_id})
    return ItemModel(**created_item)
