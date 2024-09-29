from pydantic import BaseModel, Field
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    age: Optional[int] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
