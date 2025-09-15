from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import settings
from .models.user import UserInDB, UserType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncIOMotorDatabase:
    """
    Dependency: Creates a new DB client for each request and closes it after.
    This is the most reliable pattern for serverless environments like Vercel.
    """
    client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    db = client.get_database("rent_me") # Changed database name here
    try:
        yield db
    finally:
        client.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> UserInDB:
    """
    Decodes JWT, validates user type, and fetches user from the correct collection.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        user_type: str = payload.get("type")
        if email is None or user_type is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = None
    if user_type == UserType.USER.value:
        user = await db["users"].find_one({"email": email})
    elif user_type == UserType.OWNER.value:
        user = await db["owners"].find_one({"email": email})

    if user is None:
        raise credentials_exception
        
    return UserInDB(**user)