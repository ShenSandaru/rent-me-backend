from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.chat import ChatModel
from typing import List

async def get_all_chats(db: AsyncIOMotorDatabase) -> List[ChatModel]:
    """Retrieves all chats from the database."""
    chats_cursor = db.get_collection("chats").find()
    chats = await chats_cursor.to_list(length=100)
    return [ChatModel(**chat) for chat in chats]

async def create_new_chat(chat_data: ChatModel, db: AsyncIOMotorDatabase) -> ChatModel:
    """Creates a new chat in the database."""
    chat_dict = chat_data.dict(by_alias=True, exclude={"id"})
    result = await db.get_collection("chats").insert_one(chat_dict)
    created_chat = await db.get_collection("chats").find_one({"_id": result.inserted_id})
    return ChatModel(**created_chat)