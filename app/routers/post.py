from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from typing import List, Optional

from sqlalchemy import func

from app.schemas import post_schema
from app.database import Session, get_db
from app import models
from app.oauth2 import get_current_user
from app.services.post import (
    get_posts_service,
    get_post_service,
    create_post_service,
    delete_post_service,
    update_post_service,
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[post_schema.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = await get_posts_service(db, current_user, limit, skip, search)

    return posts


@router.get("/{id}", response_model=post_schema.PostOut)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = await get_post_service(id, db, current_user)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
async def create_post(
    post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = await create_post_service(post, db, current_user)

    return new_post


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    await delete_post_service(id, db, current_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post_schema.Post)
async def update_post(
    id: int,
    post: post_schema.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = await update_post_service(id, post, db, current_user)

    return post_query.first()
