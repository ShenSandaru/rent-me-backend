from fastapi import FastAPI
from app.routes import auth, users, items, chats, rentals, payments
from fastapi import FastAPI
from app.routes import locations
from app.routes.locations import router as locations_router
from app.services.location_service import create_geo_index

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0"
)

# Include routers (assuming you have auth router too)
app.include_router(locations_router)

# On startup
@app.on_event("startup")
def startup_event():
    create_geo_index()  # Ensure geo index exists



# Register the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chats.router)
app.include_router(rentals.router)
app.include_router(payments.router)
app.include_router(locations.router)