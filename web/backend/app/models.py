from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str

class UserData(BaseModel):
    username: str
    password: str