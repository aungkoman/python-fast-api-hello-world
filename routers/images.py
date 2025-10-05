from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import ImageInDB, UserInDB
from services import image_service
from routers.users import get_current_user

router = APIRouter()

@router.post("/images/upload", response_model=ImageInDB, status_code=status.HTTP_201_CREATED)
async def upload_image_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Upload an image file."""
    return await image_service.upload_image(db, file)

@router.get("/images/{image_id}", response_model=ImageInDB)
async def get_image_endpoint(image_id: str, db: Session = Depends(get_db)):
    """Retrieve image metadata by ID."""
    db_image = image_service.get_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return db_image

@router.get("/images", response_model=List[ImageInDB])
async def get_all_images_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all image metadata."""
    images = image_service.get_images(db, skip=skip, limit=limit)
    return images

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_endpoint(image_id: str, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    """Delete an image by ID."""
    db_image = image_service.delete_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return None