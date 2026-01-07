from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.v1.endpoints import kaggle_cron, api_keys
from api.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(kaggle_cron.router, prefix="/api/v1/cron", tags=["cron"])
app.include_router(api_keys.router, prefix="/api/v1", tags=["config"])

@app.get("/")
def root():
    return {"message": "Kaggle Automation API is running"}
