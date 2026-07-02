from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
import aiofiles
import logging

from helpers.config import Settings, get_settings
from controllers import DataController, ProcessController
from models import ResponseSignal
from .schemas.data import DataRequest

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
        
        file_path, random_filename = DataController().generate_unique_filepath(file.filename, project_id)

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
                "response_signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": random_filename
          }
        )
    
@data_router.post("/process/{project_id}")
async def process_data(project_id: str, data_request: DataRequest):
    file_id = data_request.file_id
    print(file_id)
    process_controller = ProcessController(project_id= project_id)
  
    file_content = process_controller.get_file_content(file_id=file_id)

    chuncks = process_controller.process_file_content(file_content=file_content, file_id=file_id)


    if chuncks == None or len(chuncks)==0:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={
                "response_signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )

    return chuncks