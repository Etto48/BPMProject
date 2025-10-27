import os
from typing import Optional
import fastapi
from pathlib import Path
import logging
from io import BytesIO
import json
from fastapi import HTTPException, Depends, Request, UploadFile
from fastapi.params import File
from fastapi.responses import JSONResponse
from database import UserRepository, ProjectRepository
from auth import hash_password, verify_password
from models import DeleteUserData, Project, ProjectInDB, QualitativeAnalysisData, Risk, RiskInDB, TrackedRisk, TrackedScoredRisk, TrackedManagedRisk, UserData, UserResponse, UserInDB, UserUpdateData

from llm import LLM # type: ignore

logger = logging.getLogger(__name__)

FILE_PATH = Path(os.getenv("BACKEND_FILE_PATH", "/data"))
ASSETS_PATH = Path("/app/assets")

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
    
    return UserResponse(id=user.id, username=user.username, companyDescription=user.companyDescription)


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
    return UserResponse(id=user.id, username=user.username, companyDescription=user.companyDescription)


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

@api.delete("/me")
async def delete_account(
    request: Request,
    user_data: DeleteUserData,
    db: UserRepository = Depends(get_user_repository)
) -> JSONResponse:
    """Delete current user account"""
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    user = await db.get_user_by_id(user_id)
    if user is None:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    
    if not verify_password(user_data.password, user.passwordHash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    deleted = await db.delete_user_by_id(user_id)
    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    request.session.clear()
    response = JSONResponse({"message": "Account deleted"})
    response.delete_cookie("session")
    return response

@api.post("/me/picture")
async def upload_profile_picture(
    request: Request,
    picture: UploadFile = File(..., description="The profile picture file to upload")):
    """Upload profile picture for current user"""
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    # Validate file type
    if not picture.content_type or not picture.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Get file extension from content type
    content_type_to_ext = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/webp': '.webp',
        'image/gif': '.gif'
    }

    file_ext = content_type_to_ext.get(picture.content_type)
    if not file_ext:
        raise HTTPException(status_code=400, detail="Unsupported image format")
    
    file_basename = f"user_{user_id}"
    file_name = f"{file_basename}{file_ext}"
    file_path = FILE_PATH / file_name

    try:
        # Delete old photo if exists
        for existing_file in FILE_PATH.glob(f"{file_basename}.*"):
            existing_file.unlink()
        
        with open(file_path, "wb") as buffer:
            buffer.write(await picture.read())

        return {"message": "Profile picture uploaded successfully"}
    
    except Exception as e:
        logger.error(f"Error saving profile picture for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload profile picture")
    
@api.delete("/me/picture")
async def delete_profile_picture(request: Request):
    """Delete profile picture for current user"""
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    file_basename = f"user_{user_id}"
    deleted = False
    # Search for existing photo with any supported extension
    for ext in ['.jpg', '.png', '.webp', '.gif']:
        file_path = FILE_PATH / f"{file_basename}{ext}"
        if file_path.exists():
            file_path.unlink()
            deleted = True
            break

    if not deleted:
        raise HTTPException(status_code=404, detail="No profile picture to delete")

    return {"message": "Profile picture deleted successfully"}

@api.get("/me/picture", responses={
    200: {"description": "Photo file", "content": {"image/*": {}}},
    401: {"description": "Not logged in"},
    404: {"description": "Profile picture not found"}
})
async def get_profile_picture(request: Request):
    """Get profile picture for current user"""
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    file_basename = f"user_{user_id}"
    ret = None
    # Search for existing photo with any supported extension
    for ext in ['.jpg', '.png', '.webp', '.gif']:
        file_path = FILE_PATH / f"{file_basename}{ext}"
        if file_path.exists():
            ret = file_path
            break

    if ret is None:
        raise HTTPException(status_code=404, detail="Profile picture not found")

    return fastapi.responses.FileResponse(ret, media_type=f"image/{ret.suffix.lstrip('.')}")

@api.post("/me", response_model=UserResponse, responses={
    200: {"description": "User profile updated successfully"},
    401: {"description": "Not logged in or invalid credentials"},
    409: {"description": "Username already exists"}
})
async def update_profile(
    request: Request,
    user_data: UserUpdateData,
    db: UserRepository = Depends(get_user_repository)
):
    """Update current user profile"""
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]
    old_user_data = await db.get_user_by_id(user_id)
    if old_user_data is None:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    
    new_username = old_user_data.username
    if user_data.username is not None:
        new_username = user_data.username

    new_company_description = old_user_data.companyDescription
    if user_data.companyDescription is not None:
        new_company_description = user_data.companyDescription

    if user_data.newPassword is not None:
        if user_data.password is None:
            raise HTTPException(
                status_code=401,
                detail="Current password required to set a new password"
            )
        if not verify_password(user_data.password, old_user_data.passwordHash):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        new_password_hash = hash_password(user_data.newPassword)
    else:
        new_password_hash = old_user_data.passwordHash

    try:
        updated_user = await db.update_user(
            user_id,
            new_username,
            new_password_hash,
            new_company_description
        )
        return UserResponse(id=updated_user.id, username=updated_user.username, companyDescription=updated_user.companyDescription)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

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

@api.delete("/projects/{project_id}")
async def delete_project(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
) -> dict:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    deleted_project = await db.delete_project_by_id(project_id, user_id)
    if not deleted_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return {"message": "Project deleted"}

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
    user_db: UserRepository = Depends(get_user_repository),
    project_db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[Risk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]
    user_in_db: UserInDB = await user_db.get_user_by_id(user_id)

    project = await project_db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    generated_risks = await llm.generate_risks(user_in_db.companyDescription, project)

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
    user_db: UserRepository = Depends(get_user_repository),
    project_db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[TrackedScoredRisk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]
    user_in_db: UserInDB = await user_db.get_user_by_id(user_id)

    project = await project_db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks = await project_db.get_project_risks(project_id, user_id)
    if not risks:
        raise HTTPException(
            status_code=404,
            detail="No risks found for the project"
        )
    
    risks = list(map(lambda r: TrackedRisk(**r.model_dump()), risks))

    scored_risks = await llm.generate_risk_scores(user_in_db.companyDescription, project, risks)

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
    user_db: UserRepository = Depends(get_user_repository),
    project_db: ProjectRepository = Depends(get_project_repository),
    llm: LLM = Depends(get_llm_client),
) -> list[TrackedManagedRisk]:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]
    user_in_db: UserInDB = await user_db.get_user_by_id(user_id)

    project = await project_db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks = await project_db.get_project_risks(project_id, user_id)
    if not risks:
        raise HTTPException(
            status_code=404,
            detail="No risks found for the project"
        )

    # Filter the risks to only those that have impact*probability > project.risk_score_threshold*100
    significant_risks = []
    insignificant_risks = []
    for risk in risks:
        tracked_risk = TrackedScoredRisk(
            id=risk.id,
            title=risk.title,
            kind=risk.kind,
            description=risk.description,
            impact=risk.impact or 1,
            probability=risk.probability or 1
        )
        risk_score = tracked_risk.impact * tracked_risk.probability
        threshold_score = (project.riskScoreThreshold or 0) * 100

        if risk_score > threshold_score:
            significant_risks.append(tracked_risk)
        else:
            insignificant_risks.append(tracked_risk)

    significant_risks = list(map(lambda r: TrackedScoredRisk(**r.model_dump()), significant_risks))

    managed_risks = await llm.generate_risk_mitigation_plan(user_in_db.companyDescription, project, significant_risks)

    return managed_risks + [TrackedManagedRisk(**r.model_dump(), contingency=None, fallback=None) for r in insignificant_risks]

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

@api.get("/projects/{project_id}/download")
async def download_project_file(
    request: Request,
    project_id: int,
    db: ProjectRepository = Depends(get_project_repository),
) :
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    user_id = request.session["user_id"]

    project : Optional[ProjectInDB] = await db.get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    risks : list[RiskInDB] = await db.get_project_risks(project_id, user_id)
    
    # Generate project file json in memory
    
    project_dict = project.model_dump(exclude={'id'})
    project_dict["risks"] = [risk.model_dump(exclude={'id'}) for risk in risks] if risks else []
    project_json = json.dumps(project_dict, indent=2)
    project_bytes = BytesIO(project_json.encode('utf-8'))

    # return a json file
    return fastapi.responses.StreamingResponse(
        project_bytes,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=project_{project_id}.json"
        }
    )
