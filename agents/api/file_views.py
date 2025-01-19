from fastapi import APIRouter, UploadFile, File

from agents.common.response import RestResponse
from agents.services import file_service

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and store it using S3 protocol.
    
    - **file**: File to upload
    """
    file_location = f"uploads/{file.filename}"
    result = await file_service.upload_file(file, file_location)
    return RestResponse(data=result)

@router.get("/files/{file_name}")
async def get_file(file_name: str):
    """
    Get a presigned URL to download a file from S3 by file name.
    
    - **file_name**: Name of the file to retrieve
    """
    return RestResponse(data=await file_service.query_file(file_name))