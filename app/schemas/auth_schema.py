from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
