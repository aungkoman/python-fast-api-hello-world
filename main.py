from fastapi import FastAPI
from routers import todos, items, users, blog_posts, categories, tags, images
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(todos.router, prefix="/api/v1", tags=["todos"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(blog_posts.router, prefix="/api/v1", tags=["blog_posts"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(tags.router, prefix="/api/v1", tags=["tags"])
app.include_router(images.router, prefix="/api/v1", tags=["images"])

@app.get("/")
async def root():
    return {"message": "Hello World"}