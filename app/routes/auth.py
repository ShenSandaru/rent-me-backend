from fastapi import APIRouter, HTTPException, status
from ..database import UsersCollection, OwnersCollection
from ..models.user import UserCreateSchema, UserLoginSchema, TokenSchema, UserType
from ..utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema):
    """
    Registers a new user or owner. An email can be registered as a user and also as an owner,
    but cannot be registered for the same role twice.
    """
    hashed_password = get_password_hash(user_data.password)
    user_document = {"email": user_data.email, "hashed_password": hashed_password, "user_type": user_data.user_type.value}
    
    # --- MODIFIED LOGIC ---
    # Check only the relevant collection for an existing email.
    if user_data.user_type == UserType.USER:
        if await UsersCollection.find_one({"email": user_data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered as a User.",
            )
        await UsersCollection.insert_one(user_document)
    else: # UserType.OWNER
        if await OwnersCollection.find_one({"email": user_data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered as an Owner.",
            )
        await OwnersCollection.insert_one(user_document)
    # --- END OF MODIFIED LOGIC ---
        
    return {"message": f"{user_data.user_type.value.capitalize()} created successfully"}

@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(form_data: UserLoginSchema):
    """Authenticates a user/owner from the specified collection and returns an access token."""
    user = None
    # Select the collection based on the provided user_type
    if form_data.user_type == UserType.USER:
        user = await UsersCollection.find_one({"email": form_data.email})
    else: # UserType.OWNER
        user = await OwnersCollection.find_one({"email": form_data.email})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for the specified user type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create and return the JWT with the user's type
    access_token = create_access_token(data={"sub": user["email"], "type": user["user_type"]})
    return {"access_token": access_token, "token_type": "bearer"}