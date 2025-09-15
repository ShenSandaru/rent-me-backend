from fastapi import APIRouter, Depends
from ..dependencies import get_current_user
from ..models.user import UserInDB

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    """
    Fetches the profile of the currently authenticated user.
    """
    return current_user