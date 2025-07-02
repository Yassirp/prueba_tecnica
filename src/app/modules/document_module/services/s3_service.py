import boto3

from fastapi import UploadFile
from src.app.shared.constants.settings import Settings

class S3Service:
    @staticmethod
    async def upload_file(file: UploadFile, filename: str) -> str:
        session = boto3.Session()
        s3 = session.client(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION,
        )
        
        content = await file.read()
        s3.put_object(
                Bucket=Settings.S3_BUCKET,
                Key=filename,
                Body=content,
                ContentType=file.content_type
            )
        return f"https://{Settings.S3_BUCKET}.s3.{Settings.AWS_REGION}.amazonaws.com/{filename}"
    
    @staticmethod
    async def delete_file(filename: str):
        session = boto3.Session()
        s3 = session.client(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION,
                    )
        s3.delete_object(
            Bucket=Settings.S3_BUCKET,
            Key=filename,
        )
        return True
    
    @staticmethod
    async def get_file(filename: str):
        session = boto3.Session()
        s3 = session.client(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION,
        )
        return s3.get_object(Bucket=Settings.S3_BUCKET, Key=filename)
    
    @staticmethod
    async def get_file_url(filename: str):
        return f"https://{Settings.S3_BUCKET}.s3.{Settings.AWS_REGION}.amazonaws.com/{filename}"