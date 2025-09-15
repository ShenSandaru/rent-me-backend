from fastapi import APIRouter, Depends
from ..dependencies import get_current_user
from ..models.user import UserInDB

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    This endpoint is protected and requires a valid JWT token.
    """
    return current_user