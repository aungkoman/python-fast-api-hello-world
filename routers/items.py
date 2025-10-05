from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from models import ItemCreate, ItemUpdate, ItemInDB
from config import settings
from database import get_db
from services import item_service

router = APIRouter()

@router.post("/items", response_model=ItemInDB, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    return item_service.create_item(db=db, item=item)

@router.get("/items", response_model=List[ItemInDB])
async def read_items(
    skip: int = 0,
    limit: int = settings.items_per_page,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve a list of items."""
    return item_service.get_items(db=db, skip=skip, limit=limit, name=name)

@router.get("/items/{item_id}", response_model=ItemInDB)
async def read_item(item_id: str, db: Session = Depends(get_db)):
    """Retrieve a single item by ID."""
    db_item = item_service.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item."""
    db_item = item_service.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str, db: Session = Depends(get_db)):
    """Delete an item."""
    db_item = item_service.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return