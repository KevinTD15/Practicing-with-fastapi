from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from typing import List

from app.schemas import vote_schema
from app.database import Session, get_db
from app import models
from app.oauth2 import get_current_user
from app.services.vote import vote_service

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: vote_schema.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    await vote_service(vote, db, current_user)
