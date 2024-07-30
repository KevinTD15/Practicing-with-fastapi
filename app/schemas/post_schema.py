from pydantic import BaseModel
from datetime import datetime
from .user_schema import User


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User


class PostOut(BaseModel):
    Post: Post
    votes: int


class PostCreate(PostBase):
    pass


class PostDelete(PostBase):
    pass


class PostUpdate(PostBase):
    pass
