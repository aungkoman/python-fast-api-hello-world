import os
import uuid
from typing import List

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from models import ImageCreate, ImageInDB
from database import get_db
from models import Image as DBImage

UPLOAD_DIRECTORY = "static/images"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def create_image(db: Session, image: ImageCreate) -> DBImage:
    db_image = DBImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: str) -> DBImage:
    return db.query(DBImage).filter(DBImage.id == image_id).first()

def get_images(db: Session, skip: int = 0, limit: int = 100) -> List[DBImage]:
    return db.query(DBImage).offset(skip).limit(limit).all()

def delete_image(db: Session, image_id: str):
    db_image = db.query(DBImage).filter(DBImage.id == image_id).first()
    if db_image:
        # Delete the file from the filesystem
        if os.path.exists(db_image.file_path):
            os.remove(db_image.file_path)
        db.delete(db_image)
        db.commit()
    return db_image

async def upload_image(db: Session, file: UploadFile) -> ImageInDB:
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

        with open(file_path, "wb") as buffer:
            while content := await file.read(1024):
                buffer.write(content)

        image_create = ImageCreate(filename=unique_filename, file_path=file_path, url=f"/{UPLOAD_DIRECTORY}/{unique_filename}")
        db_image = create_image(db, image_create)
        return ImageInDB.from_orm(db_image)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not upload image: {e}")