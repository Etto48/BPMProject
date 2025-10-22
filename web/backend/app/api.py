import fastapi
import logging
from fastapi import HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from database import UserRepository
from auth import hash_password, verify_password
from models import UserData, UserResponse, UserInDB

logger = logging.getLogger(__name__)

api = fastapi.APIRouter(prefix="/api")


def get_db(request: Request) -> UserRepository:
    """Dependency to get database connection"""
    return UserRepository(request.app.state.db)


async def get_current_user(request: Request, db: UserRepository = Depends(get_db)) -> UserResponse:
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
            status_code=401,
            detail="User not found"
        )
    
    return user


@api.post("/register", response_model=UserResponse)
async def register(user_data: UserData, db: UserRepository = Depends(get_db)):
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
    
    logger.info(f"User {user.username} registered successfully")
    return user


@api.post("/login")
async def login(
    request: Request,
    user_data: UserData,
    db: UserRepository = Depends(get_db)
):
    """Login user and create session"""
    # Get user from database
    db_user_data = await db.get_user_by_username(user_data.username)
    
    if db_user_data is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    user_id = db_user_data.id
    stored_username = db_user_data.username
    password_hash = db_user_data.password_hash

    # Verify password
    if not verify_password(user_data.password, password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Create session
    request.session["user_id"] = user_id
    request.session["username"] = stored_username
    logger.info(f"User {user_data.username} logged in successfully")
    
    return {"message": "Logged in"}


@api.get("/me", response_model=UserResponse)
async def me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@api.get("/logout")
def logout(request: Request):
    """Logout user and clear session"""
    username = request.session.get("username")
    if username:
        logger.info(f"User {username} logged out")

    request.session.clear()
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("session")
    return response
