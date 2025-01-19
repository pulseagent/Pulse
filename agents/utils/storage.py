from abc import ABC, abstractmethod

# import boto3
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from agents.models.models import FileStorage


class Storage(ABC):
    @abstractmethod
    def upload_file(self, file: UploadFile, file_location: str) -> dict:
        pass

    @abstractmethod
    def delete_file(self, file_location: str) -> dict:
        pass

    @abstractmethod
    def get_file_url(self, file_location: str, expiration: int = 3600) -> str:
        pass

    @staticmethod
    def get_storage():
        storage = DatabaseStorage()
        return storage

    # class S3Storage(Storage):
#     def __init__(self, bucket_name: str):
#         self.s3_client = boto3.client('s3')
#         self.bucket_name = bucket_name
#
#     def upload_file(self, file: UploadFile, file_location: str) -> dict:
#         """
#         Upload a file to S3.
#
#         :param file: The file to upload
#         :param file_location: The location in the bucket to store the file
#         :return: A dictionary with the upload result
#         """
#         self.s3_client.upload_fileobj(file.file, self.bucket_name, file_location)
#         return {"message": "File uploaded successfully", "file_location": file_location}

    def file_exists(self, file_location: str) -> bool:
        """
        Check if a file exists in S3.

        :param file_location: The location in the bucket to check
        :return: True if the file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_location)
            return True
        except self.s3_client.exceptions.ClientError:
            return False

    def delete_file(self, file_location: str) -> dict:
        """
        Delete a file from S3.

        :param file_location: The location in the bucket of the file to delete
        :return: A dictionary with the delete result
        """
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_location)
        return {"message": "File deleted successfully", "file_location": file_location}

    def get_file_url(self, file_location: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL to download a file from S3.

        :param file_location: The location in the bucket of the file
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: A presigned URL to download the file
        """
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_location},
            ExpiresIn=expiration
        )
        return url

class DatabaseStorage(Storage):
    def __init__(self, session: AsyncSession):
        self.db_session = session

    def upload_file(self, file: UploadFile, file_location: str) -> dict:
        file_content = file.file.read()
        new_file = FileStorage(file_name=file.filename, file_content=file_content)
        self.db_session.add(new_file)
        self.db_session.commit()
        return {"message": "File uploaded to database", "file_location": file_location}

    def delete_file(self, file_location: str) -> dict:
        file_record = self.db_session.query(FileStorage).filter_by(file_name=file_location).first()
        if file_record:
            self.db_session.delete(file_record)
            self.db_session.commit()
            return {"message": "File deleted from database", "file_location": file_location}
        return {"error": "File not found in database", "file_location": file_location}

    def get_file_url(self, file_location: str, expiration: int = 3600) -> str:
        file_record = self.db_session.query(FileStorage).filter_by(file_name=file_location).first()
        if file_record:
            return file_record.file_content
        return "File not found in database"
