from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str

class UserData(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    password_hash: str