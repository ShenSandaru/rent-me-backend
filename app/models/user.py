from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Any
from bson import ObjectId
from datetime import datetime
from enum import Enum
from pydantic_core import core_schema

class UserType(str, Enum):
    USER = "user"
    OWNER = "owner"

# This custom class handles MongoDB ObjectId validation, serialization,
# and JSON schema generation for Pydantic v2.
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(
                                cls.validate
                            ),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    email: EmailStr
    hashed_password: str
    user_type: UserType
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    # Use model_config in Pydantic v2 instead of the old Config class
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}, # Kept for compatibility, but PyObjectId handles it
    )

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    user_type: UserType

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
    user_type: UserType

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    user_type: UserType

class TokenSchema(BaseModel):
    access_token: str
    token_type: str