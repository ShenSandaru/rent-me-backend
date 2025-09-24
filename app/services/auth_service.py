from fastapi import HTTPException, status
from ..models.user import UserLoginSchema, UserType, TokenSchema
from ..utils.security import verify_password, create_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase

async def login_user(form_data: UserLoginSchema, db: AsyncIOMotorDatabase) -> TokenSchema:
    """Authenticates a user/owner and returns an access token."""
    collection_name = "users" if form_data.user_type == UserType.USER else "owners"
    user = await db[collection_name].find_one({"email": form_data.email})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for the specified user type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"], "type": user["user_type"]})
    return TokenSchema(access_token=access_token, token_type="bearer")
