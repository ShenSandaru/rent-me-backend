from fastapi import APIRouter, Depends
from ..database import get_database
from ..models.chat import ChatModel
from typing import List
from ..services import chat_service
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.get("/", response_model=List[ChatModel])
async def get_chats(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await chat_service.get_all_chats(db)

@router.post("/", response_model=ChatModel)
async def create_chat(chat: ChatModel, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await chat_service.create_new_chat(chat, db)