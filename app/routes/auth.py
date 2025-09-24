from fastapi import APIRouter, status, Depends
from ..models.user import UserCreateSchema, UserLoginSchema, TokenSchema
from ..services import user_service, auth_service
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..database import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Registers a new user or owner by calling the user service.
    """
    return await user_service.create_user(user_data, db)

@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(form_data: UserLoginSchema, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Authenticates a user/owner and returns an access token
    by calling the authentication service.
    """
    return await auth_service.login_user(form_data, db)