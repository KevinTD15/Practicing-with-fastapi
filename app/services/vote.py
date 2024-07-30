from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from typing import List

from app.schemas import vote_schema
from app.database import Session, get_db
from app import models
from app.oauth2 import get_current_user


async def vote_service(
    vote: vote_schema.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    v = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id
    )
    if v.first():
        if vote.vote_dir == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You alredy liked the requested post",
            )
        v.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post disliked successfully"}
    else:
        if vote.vote_dir == 1:
            new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You can't dislike a post if you haven't liked it first",
        )
