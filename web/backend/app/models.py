from pydantic import BaseModel, Field
from typing import Optional, Literal

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

class Project(BaseModel):
    name: str
    description: str

class ProjectInDB(Project):
    id: int

class Risk(BaseModel):
    type: Literal['threat', 'opportunity'] = Field(
        description="'threat' for negative risks, 'opportunity' for positive risks"
    )
    
    title: str = Field(
        description="Concise risk title (maximum 4-5 words)"
    )
    
    description: str = Field(
        description="Detailed description of what the risk entails and the context that causes it"
    )

class RiskInDB(Risk):
    id: int
    project_id: int