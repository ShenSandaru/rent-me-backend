from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase

from .config import settings
from .models.user import UserInDB, UserType
from .database import get_database # Import the new dependency function

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# The dependency is now just the imported function
get_db = get_database

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
    
    db = get_db() # Get the database instance
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available.")

    user = None
    if user_type == UserType.USER.value:
        user = await db["users"].find_one({"email": email})
    elif user_type == UserType.OWNER.value:
        user = await db["owners"].find_one({"email": email})

    if user is None:
        raise credentials_exception
        
    return UserInDB(**user)