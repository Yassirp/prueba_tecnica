import boto3
import sys
import os
import base64
import mimetypes
import uuid
import unicodedata
import re
from fastapi import UploadFile
from botocore.exceptions import NoCredentialsError, ClientError
from pprint import pprint
from typing import Any, Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

from io import BytesIO
load_dotenv()


def dd(var: Any) -> None:
    pprint(var)
    sys.exit()


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str is None:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

def slugify(value):
    # Convierte texto a ascii, elimina caracteres no permitidos y reemplaza espacios por guiones bajos
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)

def upload_base64_to_s3_with_structure(
    base64_data: str,
    environment: str,
    project_name: str,
    entity_type_name: str,
    stage_name: str,
    entity_id: int,
    document_type_id: int,
    document_type_name: str,
) -> str:
    try:
        # Validar y procesar base64
        if not base64_data.startswith("data:"):
            raise Exception("El contenido base64 no contiene un encabezado válido (data:mimetype;base64,...)")

        header, encoded = base64_data.split(",", 1)
        mime_type = header.split(":")[1].split(";")[0]
        ext = mimetypes.guess_extension(mime_type) or ".bin"
        
        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        short_uuid = str(uuid.uuid4()).split('-')[0]
        base_name = f"{document_type_name}_{now}_{str(uuid.uuid4()).split('-')[0]}_{document_type_id}_{document_type_name}"
        
        # Aplica slugify para evitar problemas con caracteres especiales
        filename = slugify(base_name) + ext

        key = ( 
            f"{environment}/{project_name}/"
            f"{entity_type_name}/{stage_name}/{entity_id}/{filename}"
        )

        file_content = base64.b64decode(encoded)
        print(
            "AWS_REGION: ",os.getenv('AWS_REGION'),
            "AWS_ACCESS_KEY_ID: ",os.getenv('AWS_ACCESS_KEY_ID'),
            "AWS_SECRET_ACCESS_KEY: ",os.getenv('AWS_SECRET_ACCESS_KEY'),
            "S3_BUCKET_NAME: ",os.getenv('S3_BUCKET_NAME'),
            f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"
        )
        s3 = boto3.client(
            "s3",
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        s3.upload_fileobj(BytesIO(file_content), os.getenv("S3_BUCKET_NAME"), key)

        file_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"
        return file_url

    except Exception as e:
        raise e
