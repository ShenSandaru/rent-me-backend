from fastapi import APIRouter, HTTPException, status
from ..database import UsersCollection, OwnersCollection
from ..models.user import UserCreateSchema, UserLoginSchema, TokenSchema, UserType
from ..utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema):
    """Registers a new user as a 'user' or 'owner', ensuring email is unique across both roles."""
    #
    # --- THIS IS THE CRITICAL LOGIC ---
    # Check if the email exists in the Users collection
    if await UsersCollection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )
    # Check if the email exists in the Owners collection
    if await OwnersCollection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )
    # --- END OF CRITICAL LOGIC ---
    
    hashed_password = get_password_hash(user_data.password)
    user_document = {"email": user_data.email, "hashed_password": hashed_password, "user_type": user_data.user_type.value}
    
    # Insert into the appropriate collection
    if user_data.user_type == UserType.USER:
        await UsersCollection.insert_one(user_document)
    else:
        await OwnersCollection.insert_one(user_document)
        
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