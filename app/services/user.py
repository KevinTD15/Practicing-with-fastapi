from fastapi.params import Depends
from typing import List

from app import models
from app.database import Session, get_db
from app.schemas import user_schema
from app.utils import hash


async def create_user_service(
    user: user_schema.UserCreate, db: Session = Depends(get_db)
):
    user.password = hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_service(id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == id).first()
