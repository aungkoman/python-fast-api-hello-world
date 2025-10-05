from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import TagCreate, TagUpdate, TagInDB, UserInDB
from services import tag_service
from routers.users import get_current_user

router = APIRouter()

@router.post("/tags", response_model=TagInDB, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Create a new tag."""
    db_tag = tag_service.get_tag_by_name(db, name=tag.name)
    if db_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag name already registered")
    return tag_service.create_tag(db=db, tag=tag)

@router.get("/tags", response_model=List[TagInDB])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of tags."""
    tags = tag_service.get_tags(db, skip=skip, limit=limit)
    return tags

@router.get("/tags/{tag_id}", response_model=TagInDB)
async def read_tag(tag_id: str, db: Session = Depends(get_db)):
    """Retrieve a single tag by ID."""
    db_tag = tag_service.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return db_tag

@router.put("/tags/{tag_id}", response_model=TagInDB)
async def update_tag(tag_id: str, tag: TagUpdate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Update an existing tag."""
    db_tag = tag_service.update_tag(db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return db_tag

@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: str, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Delete a tag."""
    db_tag = tag_service.delete_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return None