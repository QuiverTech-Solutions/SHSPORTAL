import boto3
from fastapi import UploadFile
from src.core.config import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_REGION,
    S3_SECRET_ACCESS_KEY,
)
from src.utils.formatters import Formatters
from src.utils.helpers import Helpers

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=str(S3_SECRET_ACCESS_KEY),
)

class S3Service:
    """Service class for S3 bucket operations in SHS web app."""

    @staticmethod
    async def upload_student_profile_image_to_bucket(
        image: UploadFile,
        student_id: str,
    ) -> str:
        """Upload a student's profile image to the S3 bucket."""
        file_extension = image.filename.split(".")[-1]
        file_name = await Helpers.generate_uuid()
        file_path = f"students/{student_id}/profile_image/{file_name}.{file_extension}"
        
        # Upload file to S3
        s3_client.upload_fileobj(
            image.file,
            S3_BUCKET_NAME,
            file_path,
        )
        
        # Return the URL to access the uploaded image
        return generate_download_url(key=file_path)

    @staticmethod
    async def upload_application_document_to_bucket(
        document: UploadFile,
        application_id: str,
    ) -> str:
        """Upload a student's application document to the S3 bucket."""
        file_extension = document.filename.split(".")[-1]
        file_name = await Helpers.generate_uuid()
        file_path = f"applications/{application_id}/documents/{file_name}.{file_extension}"
        
        # Upload file to S3
        s3_client.upload_fileobj(
            document.file,
            S3_BUCKET_NAME,
            file_path,
        )
        
        # Return the URL to access the uploaded document
        return generate_download_url(key=file_path)

def generate_download_url(*, key: str) -> str:
    """Generate a download URL for a file in the S3 bucket."""
    return f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{key}"
