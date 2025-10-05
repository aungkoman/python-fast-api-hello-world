from sqlalchemy.orm import Session
from models import BlogPost, BlogPostCreate, BlogPostUpdate, User, Category, Tag, BlogPostTag
from typing import List, Optional
import uuid
from datetime import datetime

def create_blog_post(db: Session, blog_post: BlogPostCreate, author_id: str):
    db_blog_post = BlogPost(
        id=str(uuid.uuid4()),
        title=blog_post.title,
        content=blog_post.content,
        author_id=author_id,
        category_id=blog_post.category_id,
        published=blog_post.published,
        published_at=blog_post.published_at,
    )
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)

    # Handle tags
    if blog_post.tag_ids:
        for tag_id in blog_post.tag_ids:
            db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if db_tag:
                blog_post_tag = BlogPostTag(blog_post_id=db_blog_post.id, tag_id=tag_id)
                db.add(blog_post_tag)
        db.commit()
        db.refresh(db_blog_post)

    return db_blog_post

def get_blog_post(db: Session, blog_post_id: str):
    return db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()

def get_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlogPost).offset(skip).limit(limit).all()

def update_blog_post(db: Session, blog_post_id: str, blog_post: BlogPostUpdate):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if db_blog_post:
        for key, value in blog_post.dict(exclude_unset=True).items():
            if key == "tag_ids":
                # Clear existing tags and add new ones
                db.query(BlogPostTag).filter(BlogPostTag.blog_post_id == blog_post_id).delete()
                if value:
                    for tag_id in value:
                        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
                        if db_tag:
                            blog_post_tag = BlogPostTag(blog_post_id=blog_post_id, tag_id=tag_id)
                            db.add(blog_post_tag)
            else:
                setattr(db_blog_post, key, value)
        db.commit()
        db.refresh(db_blog_post)
    return db_blog_post

def delete_blog_post(db: Session, blog_post_id: str):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if db_blog_post:
        db.delete(db_blog_post)
        db.commit()
    return db_blog_post