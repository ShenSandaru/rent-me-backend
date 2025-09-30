from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .user import PyObjectId # Import PyObjectId

class MessageModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    sender_id: PyObjectId # Use PyObjectId
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    participant_ids: List[PyObjectId] # Use PyObjectId
    messages: List[MessageModel] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class MessageCreateSchema(BaseModel):
    content: str