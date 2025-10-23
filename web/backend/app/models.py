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
    passwordHash: str

class Project(BaseModel):
    title: str
    description: str

class ProjectInDB(Project):
    id: int
    currentStep: int

class Risk(BaseModel):
    kind: Literal['threat', 'opportunity'] = Field(
        description="'threat' for negative risks, 'opportunity' for positive risks"
    )
    
    title: str = Field(
        description="Concise risk title (maximum 4-5 words)"
    )
    
    description: str = Field(
        description="Detailed description of what the risk entails and the context that causes it"
    )

class ScoredRisk(Risk):
    impact: float = Field(
        description="Numerical risk score between 1 and 10 indicating the impact of the risk"
    )
    probability: float = Field(
        description="Numerical probability score between 1 and 10 indicating the likelihood of the risk occurring"
    )

class ManagedRisk(ScoredRisk):
    contingency: Optional[str] = Field(
        default=None,
        description="Contingency plan describing preventive actions to avoid the risk from occurring"
    )
    fallback: Optional[str] = Field(
        default=None,
        description="Fallback plan describing actions to minimize damage if the risk occurs"
    )

class RiskInDB(BaseModel):
    id: int
    projectId: int
    kind: Literal['threat', 'opportunity']
    title: str
    description: str
    impact: Optional[int]
    probability: Optional[int]
    contingency: Optional[str]
    fallback: Optional[str]
