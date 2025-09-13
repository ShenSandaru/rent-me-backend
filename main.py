from fastapi import FastAPI
from app.routes import auth
import uvicorn

app = FastAPI(title="FastAPI MongoDB CRUD")
# Register routes
app.include_router(auth.router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)