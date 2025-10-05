from fastapi import FastAPI
from routers import todos, items, users, blog_posts, categories, tags, images
from config import settings
from database import engine
from models import User, BlogPost, Category, Tag, Image
from sqladmin import Admin, ModelView

app = FastAPI(title=settings.app_name)

admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.full_name, User.is_active, User.created_at, User.updated_at]

class BlogPostAdmin(ModelView, model=BlogPost):
    column_list = [BlogPost.id, BlogPost.title, BlogPost.author_id, BlogPost.category_id, BlogPost.published, BlogPost.published_at, BlogPost.created_at, BlogPost.updated_at]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.description, Category.created_at, Category.updated_at]

class TagAdmin(ModelView, model=Tag):
    column_list = [Tag.id, Tag.name, Tag.created_at, Tag.updated_at]

class ImageAdmin(ModelView, model=Image):
    column_list = [Image.id, Image.url, Image.alt_text, Image.created_at, Image.updated_at]

admin.add_view(UserAdmin)
admin.add_view(BlogPostAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(TagAdmin)
admin.add_view(ImageAdmin)

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