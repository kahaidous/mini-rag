from fastapi import APIRouter, Depends
from helpers.config import Settings, get_settings

base_router = APIRouter(
    prefix="/api",
    tags=["Base"]
)

@base_router.get("/check")
async def check(app_settings: Settings = Depends(get_settings)):
    return {
        "app_name": app_settings.APP_NAME,
        "app_version": app_settings.APP_VERSION
    }