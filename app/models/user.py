from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str