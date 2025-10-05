from fastapi import FastAPI
from routers import todos, items, users
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(todos.router, prefix="/api/v1", tags=["todos"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}