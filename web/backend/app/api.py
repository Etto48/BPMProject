from typing import Optional
import fastapi
import logging
from fastapi import HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from database import UserRepository, ProjectRepository
from auth import hash_password, verify_password
from models import Project, ProjectInDB, Risk, RiskInDB, UserData, UserResponse, UserInDB

logger = logging.getLogger(__name__)

api = fastapi.APIRouter(prefix="/api")


def get_user_repository(request: Request) -> UserRepository:
    """Dependency to get database connection"""
    return UserRepository(request.app.state.db)

def get_project_repository(request: Request) -> ProjectRepository:
    """Dependency to get project database connection"""
    return ProjectRepository(request.app.state.db)


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
    project = await db.create_project(project_data, user_id)

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

    # Here you would normally call the LLM to generate risks based on the project details.
    # For demonstration, we'll return a placeholder response.

    generated_risks = [
        Risk(
            type="threat",
            title="Budget Overrun",
            description="The project may exceed its allocated budget due to unforeseen expenses."
        ),
        Risk(
            type="opportunity",
            title="Market Expansion",
            description="The project could open up opportunities to enter new markets and increase revenue."
        )
                       ]

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

    added_risks = await db.add_project_risks(project_id, user_id, risks_data)
    if not added_risks:
        raise HTTPException(
            status_code=409,
            detail="Failed to add risks"
        )

    return {"message": "Risks added", "risks": added_risks}