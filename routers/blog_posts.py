from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import BlogPostCreate, BlogPostUpdate, BlogPostInDB, UserInDB
from services import blog_post_service
from routers.users import get_current_user

router = APIRouter()

@router.post("/blog_posts", response_model=BlogPostInDB, status_code=status.HTTP_201_CREATED)
async def create_blog_post(blog_post: BlogPostCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Create a new blog post."""
    return blog_post_service.create_blog_post(db=db, blog_post=blog_post, author_id=current_user.id)

@router.get("/blog_posts", response_model=List[BlogPostInDB])
async def read_blog_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of blog posts."""
    blog_posts = blog_post_service.get_blog_posts(db, skip=skip, limit=limit)
    return blog_posts

@router.get("/blog_posts/{blog_post_id}", response_model=BlogPostInDB)
async def read_blog_post(blog_post_id: str, db: Session = Depends(get_db)):
    """Retrieve a single blog post by ID."""
    db_blog_post = blog_post_service.get_blog_post(db, blog_post_id=blog_post_id)
    if db_blog_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    return db_blog_post

@router.put("/blog_posts/{blog_post_id}", response_model=BlogPostInDB)
async def update_blog_post(blog_post_id: str, blog_post: BlogPostUpdate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Update an existing blog post."""
    db_blog_post = blog_post_service.get_blog_post(db, blog_post_id=blog_post_id)
    if db_blog_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    if db_blog_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog post")
    return blog_post_service.update_blog_post(db=db, blog_post_id=blog_post_id, blog_post=blog_post)

@router.delete("/blog_posts/{blog_post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(blog_post_id: str, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Delete a blog post."""
    db_blog_post = blog_post_service.get_blog_post(db, blog_post_id=blog_post_id)
    if db_blog_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    if db_blog_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog post")
    blog_post_service.delete_blog_post(db, blog_post_id=blog_post_id)
    return None