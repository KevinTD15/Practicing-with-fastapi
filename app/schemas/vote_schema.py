from typing import Literal
from pydantic import BaseModel, EmailStr
from datetime import datetime


class Vote(BaseModel):
    post_id: int
    vote_dir: Literal[0, 1]
