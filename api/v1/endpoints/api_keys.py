from fastapi import APIRouter
from api.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/config")
def get_client_config():
    """
    Returns client configuration including API keys and Project ID.
    """
    return {
        "api_keys": settings.API_KEYS,
        "gemini_project_id": settings.GEMINI_PROJECT_ID
    }
