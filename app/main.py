from fastapi import FastAPI
from app.routes import auth, users # Make sure to import users as well
import uvicorn

app = FastAPI(
    title="RentMe API",
    description="API for a rental application.",
    version="1.0.0"
)

# Register the routers
app.include_router(auth.router)
app.include_router(users.router)

if __name__ == "__main__":
    # This block is less common for FastAPI, but for it to work,
    # you must run `python -m app.main` from the root directory.
    # The standard is to use uvicorn directly.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)