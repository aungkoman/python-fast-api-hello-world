from fastapi import FastAPI
from routers import todos
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(todos.router, prefix="/api/v1", tags=["todos"])

@app.get("/")
async def root():
    return {"message": "Hello World"}