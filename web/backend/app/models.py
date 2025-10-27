from pydantic import BaseModel, Field, RootModel, create_model
from typing import Optional, Literal

class UserResponse(BaseModel):
    id: int
    username: str
    companyDescription: str

class UserData(BaseModel):
    username: str
    password: str
    companyDescription: str = ""

class DeleteUserData(BaseModel):
    password: str

class UserUpdateData(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    companyDescription: Optional[str] = None
    newPassword: Optional[str] = None

class UserInDB(BaseModel):
    id: int
    username: str
    passwordHash: str
    companyDescription: str

class Project(BaseModel):
    title: str
    description: str

class ProjectInDB(Project):
    id: int
    currentStep: int
    riskScoreThreshold: float

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

class Risks(RootModel):
    root: list[Risk]

class TrackedRisk(Risk):
    id: int

class ImpactAndProbability(BaseModel):
    impact: int = Field(
        description="Numerical risk score proportional to the monetary impact of the risk",
        ge=1,
        le=10
    )
    probability: int = Field(
        description="Numerical probability score proportional to the likelihood of the risk occurring",
        ge=1,
        le=10
    )

class TrackedScoredRisk(TrackedRisk, ImpactAndProbability):
    ...

class QualitativeAnalysisData(BaseModel):
    risks: list[TrackedScoredRisk]
    riskScoreThreshold: float

class ContingencyAndFallback(BaseModel):
    contingency: Optional[str] = Field(
        default=None,
        description="Contingency plan describing preventive actions to avoid the risk from occurring"
    )
    fallback: Optional[str] = Field(
        default=None,
        description="Fallback plan describing actions to minimize damage if the risk occurs"
    )

class TrackedManagedRisk(TrackedScoredRisk, ContingencyAndFallback):
    ...

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

def generate_risk_score_model(risks: list[TrackedRisk]):    
    fields = {
        f"risk_{risk.id}": (ImpactAndProbability, 
            Field(..., description=f"Risk impact and probability for risk with ID {risk.id} ({risk.title})")) for risk in risks
    }
    return create_model(
        "RiskScores",
        **fields
    )

def generate_managed_risk_model(risks: list[TrackedScoredRisk]):    
    fields = {
        f"risk_{risk.id}": (ContingencyAndFallback, 
            Field(..., description=f"Contingency and fallback plans for risk with ID {risk.id} ({risk.title})")) for risk in risks
    }
    return create_model(
        "ManagedRisks",
        **fields
    )