from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import CategoryCreate, CategoryUpdate, CategoryInDB, UserInDB
from services import category_service
from routers.users import get_current_user

router = APIRouter()

@router.post("/categories", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Create a new category."""
    db_category = category_service.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already registered")
    return category_service.create_category(db=db, category=category)

@router.get("/categories", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of categories."""
    categories = category_service.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: str, db: Session = Depends(get_db)):
    """Retrieve a single category by ID."""
    db_category = category_service.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.put("/categories/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: CategoryUpdate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Update an existing category."""
    db_category = category_service.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Delete a category."""
    db_category = category_service.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return None