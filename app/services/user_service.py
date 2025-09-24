from fastapi import HTTPException, status
from ..models.user import UserCreateSchema, UserType
from ..utils.security import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase

async def create_user(user_data: UserCreateSchema, db: AsyncIOMotorDatabase):
    collection_name = "users" if user_data.user_type == UserType.USER else "owners"
    collection = db.get_collection(collection_name)
    
    if await collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This email is already registered as a {user_data.user_type.value}.",
        )
        
    hashed_password = get_password_hash(user_data.password)
    user_document = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "user_type": user_data.user_type.value
    }
    
    await collection.insert_one(user_document)
    return {"message": f"{user_data.user_type.value.capitalize()} created successfully"}
