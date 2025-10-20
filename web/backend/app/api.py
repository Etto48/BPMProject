import fastapi
import logging

logger = logging.getLogger(__name__)

api = fastapi.APIRouter(prefix="/api")
