from fastapi import status, HTTPException, APIRouter
from fastapi.exceptions import ResponseValidationError
from fastapi.params import Depends
from typing import List

from fastapi.responses import JSONResponse

from app import models
from app.database import Session, get_db
from app.schemas import user_schema
from app.utils import hash
from app.services.user import create_user_service, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return await create_user_service(user, db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
        )


@router.get("/{id}", response_model=user_schema.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = await get_user_service(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} was not found",
        )
    return user
