import os
import fastapi
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import logging
import psycopg

from api import api
from mockups.llm import LLM

logger = logging.getLogger(__name__)

LLM_HOST = os.getenv("LLM_HOST", "http://localhost:8000")
LLM_PORT = os.getenv("LLM_PORT", "11434")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:latest")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "aira")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey") # In production, use a secure key from environment variables

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    app.state.db = await psycopg.AsyncConnection.connect(
        f"host={DB_HOST} port={DB_PORT} user={DB_USER} password={DB_PASSWORD} dbname={DB_NAME}",
        autocommit=True
    )
    logger.info("Database connection established.")
    app.state.llm = LLM(
        url=f"http://{LLM_HOST}:{LLM_PORT}/v1",
        model=LLM_MODEL,
        api_key=LLM_API_KEY
    )
    logger.info("LLM client initialized.")
    yield
    await app.state.db.close()
    logger.info("Database connection closed.")

app = fastapi.FastAPI(lifespan=lifespan, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,  # In production, use a secure key from environment variables
    max_age=14 * 24 * 60 * 60,  # 14 days in seconds
    same_site="lax",
    https_only=False,  # Set to True in production with HTTPS
    path="/",
    domain=None  # Let the browser determine the domain
)
app.include_router(api)
