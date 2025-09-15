from fastapi import FastAPI
from app.routes import auth, users

# The lifespan manager is removed. The app setup is minimal.
app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0"
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)