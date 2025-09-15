from fastapi import APIRouter, HTTPException, status
from ..database import UserCollection
from ..models.user import UserCreateSchema, UserLoginSchema, TokenSchema
from ..utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema):
    """Registers a new user."""
    # Check if user already exists
    existing_user = await UserCollection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash the password and create the user document
    hashed_password = get_password_hash(user_data.password)
    user_document = {"email": user_data.email, "hashed_password": hashed_password}
    
    await UserCollection.insert_one(user_document)
    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(form_data: UserLoginSchema):
    """Authenticates a user and returns an access token."""
    user = await UserCollection.find_one({"email": form_data.email})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create and return the JWT
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}