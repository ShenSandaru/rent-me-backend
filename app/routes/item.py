from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login():
    return {"message": "User logged in"}

@router.get("/register")
async def register():
    return {"message": "User registered"}
