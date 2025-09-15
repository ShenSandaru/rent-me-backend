from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.chat import ChatModel
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.get("/", response_model=List[ChatModel])
async def get_chats():
    chats = await db.Chats.find().to_list(100)
    return chats

@router.post("/", response_model=ChatModel)
async def create_chat(chat: ChatModel):
    chat_dict = chat.dict(by_alias=True)
    if chat_dict.get("_id") is None:
        chat_dict.pop("_id", None)
    result = await db.Chats.insert_one(chat_dict)
    chat_dict["_id"] = result.inserted_id
    return chat_dict