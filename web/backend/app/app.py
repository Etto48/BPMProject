import fastapi
from fastapi.concurrency import asynccontextmanager
import logging

from api import api

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    yield

app = fastapi.FastAPI(lifespan=lifespan, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
app.include_router(api)
