import os
import fastapi
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
import logging
import psycopg

from api import api

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "aira")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    app.state.db = await psycopg.AsyncConnection.connect(
        f"host={DB_HOST} port={DB_PORT} user={DB_USER} password={DB_PASSWORD} dbname={DB_NAME}"
    )
    logger.info("Database connection established.")
    yield
    await app.state.db.close()
    logger.info("Database connection closed.")

app = fastapi.FastAPI(lifespan=lifespan, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
app.add_middleware(SessionMiddleware, secret_key="supersecretkey") # In production, use a secure key from environment variables
app.include_router(api)
