from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kaggle Automation Cron"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Kaggle Credentials
    KAGGLE_USERNAME: str
    KAGGLE_KEY: str
    
    # Musetalk Paths
    NB_PATH: str = "data/musetalk-v1.ipynb"
    METADATA_PATH: str = "data/kernel-metadata.json"

    # VoxCPM Credentials
    VOXCPM_USERNAME: str | None = None
    VOXCPM_KEY: str | None = None
    
    # VoxCPM Paths
    VOXCPM_NB_PATH: str = "data/voxcpm/voxcpm-api.ipynb"
    VOXCPM_METADATA_PATH: str = "data/voxcpm/kernel-metadata.json"

    # Client Config
    API_KEYS: list[str] = [
        'AIzaSyAOWknOS2YWTdspM0CKfQT0uxMrBP8cg00',
        'AIzaSyAtfDRIjNz-Pt4BD-AsV4wlvWh7hD1qzWc',
        'AIzaSyDM181FEzSQ3VO3TSPKT_y1rIKwDo_90EY',
        'AIzaSyD9QB87596GPXYrDENkkIgBggw-RbFjsR0',
        'AIzaSyBLY-i5eYox7x26eWjgaHX-7b7rS_B3eBY',
        'AIzaSyAMmJaUuXfQprZcOx6WrycPtXVRVEvB6hs'
    ]
    GEMINI_PROJECT_ID: str = 'gen-lang-client-0221138162'


    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
