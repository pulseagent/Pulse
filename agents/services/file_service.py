from fastapi import UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agents.models.db import get_db
from agents.utils.storage import DatabaseStorage

async def upload_file(file: UploadFile, file_location: str, session: AsyncSession = Depends(get_db)):
    storage = DatabaseStorage(session)
    return storage.upload_file(file, file_location)

async def query_file(file_name: str, session: AsyncSession = Depends(get_db)):
    storage = DatabaseStorage(session)
    file_record = session.query(storage).filter_by(file_name=file_name).first()
    if file_record:
        return {"file_name": file_record.file_name, "file_content": file_record.file_content}
    return {"error": "File not found"}
