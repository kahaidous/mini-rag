from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
import aiofiles
import os
import logging

from helpers.config import Settings, get_settings
from controllers import DataController
from models import ResponseSignal

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/data",
    tags=["Data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, 
                      file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    is_valid, response_signal = DataController().validate_upload_file(file) 
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "is_valid": is_valid,
                "response_signal": response_signal.value
            }
        )
    else:
        
        file_path = DataController().generate_unique_filename(file.filename, project_id)

        try:
            async with aiofiles.open(file_path, 'wb') as out_file:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await out_file.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file {file.filename} for project {project_id}: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "response_signal": ResponseSignal.FILE_UPLOAD_FAILED.value,
                }
            )
         
        return JSONResponse(
            content={
                "is_valid": is_valid,
                "response_signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
          }
        )