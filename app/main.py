from fastapi import FastAPI
from app.routes import auth, users, items, chats, rentals, payments
import uvicorn

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0"
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chats.router)
app.include_router(rentals.router)
app.include_router(payments.router)

if __name__ == "__main__":
    # This block is less common for FastAPI, but for it to work,
    # you must run `python -m app.main` from the root directory.
    # The standard is to use uvicorn directly.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)