from fastapi import FastAPI
from app.routes import auth, users

# No more database or lifespan imports needed here

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0",
    # The lifespan attribute is removed
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)