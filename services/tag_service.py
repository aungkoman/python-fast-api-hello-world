from sqlalchemy.orm import Session
from models import Tag, TagCreate, TagUpdate
from typing import List, Optional
import uuid
from datetime import datetime

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(
        id=str(uuid.uuid4()),
        name=tag.name,
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tag(db: Session, tag_id: str):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()

def update_tag(db: Session, tag_id: str, tag: TagUpdate):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag:
        for key, value in tag.dict(exclude_unset=True).items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: str):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag