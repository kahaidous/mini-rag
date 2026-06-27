from fastapi import APIRouter
import os
base_router = APIRouter(
    prefix="/api",
    tags=["Base"]
)

@base_router.get("/check")
def check():
    api_name = os.getenv('APP_NAME')
    api_version = os.getenv('APP_VERSION')
    return {
        "api_name": api_name,
        "api_version": api_version
    }