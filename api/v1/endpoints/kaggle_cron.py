from fastapi import APIRouter, HTTPException, Depends
from api.services.kaggle_service import KaggleService

from api.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/run-kaggle")
def run_musetalk_automation():
    try:
        # Default uses Musetalk settings from config/env
        service = KaggleService() 
        # Clean metadata to avoid conflicts with stale id_no or docker_image
        result = service.prepare_and_push(clean_metadata=True)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/run-voxcpm")
def run_voxcpm_automation():
    try:
        service = KaggleService(
            username=settings.VOXCPM_USERNAME,
            key=settings.VOXCPM_KEY,
            nb_path=settings.VOXCPM_NB_PATH,
            metadata_path=settings.VOXCPM_METADATA_PATH
        )
        # Clean metadata for VoxCPM to force new kernel/avoid conflicts
        result = service.prepare_and_push(clean_metadata=True)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
