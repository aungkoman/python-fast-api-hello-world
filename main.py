from fastapi import FastAPI
from routers import todos, items
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(todos.router, prefix="/api/v1", tags=["todos"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Hello World"}