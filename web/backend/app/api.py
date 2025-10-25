from typing import Optional
import fastapi
import logging
from fastapi import HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from database import UserRepository, ProjectRepository
from auth import hash_password, verify_password
from models import Project, ProjectInDB, QualitativeAnalysisData, Risk, RiskInDB, TrackedRisk, TrackedScoredRisk, TrackedManagedRisk, UserData, UserResponse, UserInDB

from llm import LLM # type: ignore

logger = logging.getLogger(__name__)

api = fastapi.APIRouter(prefix="/api")


def get_user_repository(request: Request) -> UserRepository:
    """Dependency to get database connection"""
    return UserRepository(request.app.state.db)

def get_project_repository(request: Request) -> ProjectRepository:
    """Dependency to get project database connection"""
    return ProjectRepository(request.app.state.db)

def get_llm_client(request: Request) -> LLM:
    """Dependency to get LLM client"""
    return request.app.state.llm

async def get_current_user(request: Request, db: UserRepository = Depends(get_user_repository)) -> UserResponse:
    """Dependency to get current authenticated user"""
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    
    user = await db.get_user_by_id(user_id)
    if user is None:
        # User no longer exists, clear session
        request.session.clear()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user


@api.post("/register", response_model=UserResponse)
async def register(request: Request, user_data: UserData, db: UserRepository = Depends(get_user_repository)):
    """Register a new user"""
    # Hash the password
    password_hash = hash_password(user_data.password)
    
    # Create user in database
    user = await db.create_user(user_data.username, password_hash)
    
    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    
    # Create session for the newly registered user
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    
    logger.info(f"User {user.username} registered successfully")
    return user


@api.post("/login")
async def login(
    request: Request,
    user_data: UserData,
    db: UserRepository = Depends(get_user_repository)
) -> JSONResponse:
    """Login user and create session"""
    logger.info(f"Login attempt for user: {user_data.username}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request cookies before: {request.cookies}")
    
    # Get user from database
    db_user_data = await db.get_user_by_username(user_data.username)
    
    if db_user_data is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    user_id = db_user_data.id
    stored_username = db_user_data.username
    passwordHash = db_user_data.passwordHash

    # Verify password
    if not verify_password(user_data.password, passwordHash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Create session
    request.session["user_id"] = user_id
    request.session["username"] = stored_username
    logger.info(f"User {user_data.username} logged in successfully")
    logger.info(f"Session data set: user_id={user_id}, username={stored_username}")
    logger.info(f"Session after setting: {dict(request.session)}")

    return JSONResponse({"message": "Logged in"})


@api.get("/me", response_model=UserResponse)
async def me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@api.get("/logout")
def logout(request: Request) -> JSONResponse:
    """Logout user and clear session"""
    username = request.session.get("username")
    if username:
        logger.info(f"User {username} logged out")

    request.session.clear()
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("session")
    return response

@api.post("/projects")
async def create_project(
    request: Request,
    project_data: Project,
    db: ProjectRepository = Depends(get_project_repository),
) -> dict:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )

    user_id = request.session["user_id"]
    project : Optional[ProjectInDB] = await db.create_project(project_data, user_id)

    if project is None:
        raise HTTPException(
            status_code=409,
            detail="Failed to create project"
        )

    return {"message": "Project created", "id": project.id}

@api.get("/projects/{project_id}")
async def get_project(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
) -> ProjectInDB:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project

@api.get("/projects")
async def list_projects(
    request: Request,
    db: ProjectRepository = Depends(get_project_repository),
) -> list[ProjectInDB]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    projects = await db.get_projects_by_user_id(user_id)
    return projects

@api.get("/projects/{project_id}/gen/risks")
async def generate_project_risks(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[Risk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    generated_risks = await llm.generate_risks(project)

    return generated_risks

@api.get("/projects/{project_id}/risks")
async def get_project_risks(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
) -> Optional[list[RiskInDB]]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks = await db.get_project_risks(project_id, user_id)

    return risks

@api.post("/projects/{project_id}/risks")
async def add_project_risk(
    request: Request,
    project_id: int,
    risks_data: list[Risk],
    db: ProjectRepository = Depends(get_project_repository),
) -> dict:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    added_risks = await db.add_project_risks(project_id, user_id, risks_data)
    if not added_risks:
        raise HTTPException(
            status_code=409,
            detail="Failed to add risks"
        )

    return {"message": "Risks added", "risks": added_risks}


@api.get("/projects/{project_id}/gen/risks/scores")
async def generate_risk_scores(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[TrackedScoredRisk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks = await db.get_project_risks(project_id, user_id)
    if not risks:
        raise HTTPException(
            status_code=404,
            detail="No risks found for the project"
        )
    
    risks = list(map(lambda r: TrackedRisk(**r.model_dump()), risks))

    scored_risks = await llm.generate_risk_scores(project, risks)

    return scored_risks

@api.post("/projects/{project_id}/risks/scores")
async def add_risk_scores(
    request: Request,
    project_id: int,
    qualitative_analysis_data: QualitativeAnalysisData,
    db: ProjectRepository = Depends(get_project_repository),
) -> dict:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    scored_risks = qualitative_analysis_data.risks
    riskScoreThreshold = qualitative_analysis_data.riskScoreThreshold
    updated_risks = await db.add_project_risks_scores(project_id, user_id, scored_risks, riskScoreThreshold)
    if not updated_risks:
        raise HTTPException(
            status_code=409,
            detail="Failed to add risk scores"
        )
    return {"message": "Risk scores added", "risks": updated_risks}

@api.get("/projects/{project_id}/gen/risks/plans")
async def generate_risk_plans(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[TrackedManagedRisk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks = await db.get_project_risks(project_id, user_id)
    if not risks:
        raise HTTPException(
            status_code=404,
            detail="No risks found for the project"
        )

    # Filter the risks to only those that have impact*probability > project.risk_score_threshold*100
    significant_risks = [risk for risk in risks if risk.impact is not None and risk.probability is not None and (risk.impact * risk.probability) > (project.riskScoreThreshold * 100)]
    
    # TODO: Call LLM to generate risk plans

    managed_risks = [
        TrackedManagedRisk(
            id=1,
            kind='threat',
            title='Supplier bankruptcy risk',
            description='Our main component supplier is facing financial difficulties due to market downturn. If they go bankrupt, we would need to find alternative suppliers, causing delays of 2-3 months in the production schedule and requiring re-certification of new components.',
            impact=8,
            probability=4,
            contingency="Identify and pre-qualify two alternative suppliers. Maintain regular communication with current supplier to monitor their financial health.",
            fallback="Activate emergency procurement from pre-qualified suppliers and expedite component re-certification process using parallel testing."
        ),
        TrackedManagedRisk(
            id=2,
            kind='opportunity',
            title='Early framework release',
            description='The UI framework we depend on is ahead of schedule and may release version 2.0 earlier than expected. This would allow us to leverage improved performance features and reduce our custom workaround code by approximately 30%.',
            impact=6,
            probability=7,
            contingency="Allocate developer time to test beta versions and prepare migration plan. Document potential breaking changes early.",
            fallback=None
        ),
        TrackedManagedRisk(
            id=3,
            kind='threat',
            title='Key developer resignation',
            description='Our lead backend developer has been approached by competitors and may leave the company. This developer holds critical knowledge about our legacy authentication system and their departure would significantly slow down the planned security upgrade.',
            impact=9,
            probability=5,
            contingency="Conduct knowledge transfer sessions and create comprehensive documentation of the authentication system. Cross-train two junior developers.",
            fallback="Hire a specialized contractor with authentication system experience and delay non-critical features to focus resources on the security upgrade."
        )
    ]

    return managed_risks

@api.post("/projects/{project_id}/risks/plans")
async def add_risk_plans(
    request: Request,
    project_id: int,
    managed_risks: list[TrackedManagedRisk],
    db: ProjectRepository = Depends(get_project_repository),
) -> dict:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    updated_risks = await db.add_project_risks_plans(project_id, user_id, managed_risks)
    if not updated_risks:
        raise HTTPException(
            status_code=409,
            detail="Failed to add risk plans"
        )
    return {"message": "Risk plans added", "risks": updated_risks}