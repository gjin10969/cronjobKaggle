from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kaggle Automation Cron"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Kaggle Credentials
    KAGGLE_USERNAME: Optional[str] = None
    KAGGLE_KEY: Optional[str] = None
    
    # Musetalk Paths
    NB_PATH: str = "data/musetalk-v1.ipynb"
    METADATA_PATH: str = "data/kernel-metadata.json"

    # VoxCPM Credentials
    VOXCPM_USERNAME: Optional[str] = None
    VOXCPM_KEY: Optional[str] = None
    
    # VoxCPM Paths
    VOXCPM_NB_PATH: str = "data/voxcpm/voxcpm-api.ipynb"
    VOXCPM_METADATA_PATH: str = "data/voxcpm/kernel-metadata.json"

    # Client Config
    # Expects comma-separated string: "KEY1,KEY2,KEY3"
    API_KEYS: str | list[str] = []
    GEMINI_PROJECT_ID: Optional[str] = None
    
    @classmethod
    def parse_api_keys(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [k.strip() for k in v.split(",") if k.strip()]
        return v or []

    # Use field_validator for Pydantic v2 or validator for v1
    # Assuming pydantic-settings uses v2 or v1 compat.
    # Let's try simple post-init or property if validation is tricky with version mismatches.
    # Actually, pydantic-settings handles comma-separated strings for list[str] automatically in many cases!
    # But to be safe and explicit:
    
    from pydantic import field_validator
    
    @field_validator("API_KEYS", mode="before")
    @classmethod
    def assemble_api_keys(cls, v):
        return cls.parse_api_keys(v)


    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
