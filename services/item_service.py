from sqlalchemy.orm import Session
from models import Item, ItemCreate, ItemUpdate
from typing import List, Optional
from uuid import uuid4

def create_item(db: Session, item: ItemCreate):
    """Create a new item in the database."""
    db_item = Item(**item.model_dump(), id=str(uuid4()))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None):
    """Retrieve a list of items from the database, with optional filtering by name."""
    query = db.query(Item)
    if name:
        query = query.filter(Item.name.contains(name))
    return query.offset(skip).limit(limit).all()

def get_item(db: Session, item_id: str):
    """Retrieve a single item by its ID from the database."""
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: str, item: ItemUpdate):
    """Update an existing item in the database."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: str):
    """Delete an item from the database."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item