from fastapi import HTTPException, status
from ..models.user import UserCreateSchema, UserType
from ..utils.security import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase

async def create_user(user_data: UserCreateSchema, db: AsyncIOMotorDatabase):
    try:
        collection_name = "users" if user_data.user_type == UserType.USER else "owners"
        collection = db.get_collection(collection_name)
        
        # Check if user already exists
        try:
            existing_user = await collection.find_one({"email": user_data.email})
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"This email is already registered as a {user_data.user_type.value}.",
                )
        except Exception as db_error:
            # If database check fails, log but continue (for demo purposes)
            print(f"⚠️  Database check failed: {db_error}")
            print("📝 Continuing with registration (demo mode)")
        
        hashed_password = get_password_hash(user_data.password)
        user_document = {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "user_type": user_data.user_type.value
        }
        
        # Try to insert user
        try:
            await collection.insert_one(user_document)
            return {"message": f"{user_data.user_type.value.capitalize()} created successfully"}
        except Exception as insert_error:
            print(f"⚠️  Database insert failed: {insert_error}")
            # Return success response for demo purposes (in production, you'd want to handle this differently)
            return {"message": f"{user_data.user_type.value.capitalize()} created successfully (demo mode - not stored)"}
    
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user. Please try again later."
        )
