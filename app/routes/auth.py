from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..dependencies import get_db
from ..models.user import (
    UserCreateSchema,
    UserLoginSchema,
    TokenSchema,
    UserType
)
from ..utils.security import (
    get_password_hash,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

  
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateSchema,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Registers a new user or owner.
    An email can be registered as a user and also as an owner,
    but cannot be registered for the same role twice.
    """
    collection_name = (
        "Users" if user_data.user_type == UserType.USER else "Owners"
    )
    collection = db[collection_name]

    if await collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"This email is already registered as a "
                f"{collection_name[:-1]}."
            ),
        )

    hashed_password = get_password_hash(user_data.password)
    user_document = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "user_type": user_data.user_type.value
    }
    await collection.insert_one(user_document)
        
    return {
        "message": (
            f"{user_data.user_type.value.capitalize()} created successfully"
        )
    }

  
@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(
    form_data: UserLoginSchema,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Authenticates a user/owner from the specified collection
    and returns an access token.
    """
    collection_name = (
        "Users" if form_data.user_type == UserType.USER else "Owners"
    )
    user = await db[collection_name].find_one({"email": form_data.email})

    if (
        not user or not verify_password(
            form_data.password, user["hashed_password"]
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for the specified user type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["email"], "type": user["user_type"]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
  
