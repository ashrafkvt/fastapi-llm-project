# app/models.py

from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    bio: Optional[str] = None
