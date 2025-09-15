from fastapi import FastAPI
from app.routes import auth, users, items, chats, rentals, payments
from app.database import lifespan

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0",
    lifespan=lifespan
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chats.router)
app.include_router(rentals.router)
app.include_router(payments.router)