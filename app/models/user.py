from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserType(str, Enum):
    USER = "user"  # Changed to lowercase
    OWNER = "owner" # Changed to lowercase

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
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