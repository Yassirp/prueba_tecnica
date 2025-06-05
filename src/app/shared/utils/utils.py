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
        # Validar formato base64
        if not base64_data.startswith("data:"):
            raise ValueError("El contenido base64 no contiene un encabezado válido (data:mimetype;base64,...)")
        
        # Separar el encabezado del contenido
        header, encoded = base64_data.split(",", 1)
        mime_type = header.split(":")[1].split(";")[0]
        
        # Corregir encabezado malformado como "/png"
        if mime_type.startswith("/"):
            mime_type = "image" + mime_type  # => "image/png"

        # Obtener extensión del mime_type
        ext = mimetypes.guess_extension(mime_type)
        if ext is None:
            ext = ".bin"  # fallback por si no se puede identificar

        # Preparar nombre del archivo
        now = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        short_uuid = str(uuid.uuid4()).split('-')[0]
        base_name = f"{document_type_name}_{now}_{short_uuid}_{document_type_id}"
        filename = f"{slugify(base_name)}{ext}"

        # Generar key (ruta en el bucket)
        key = f"{environment}/{project_name}/{entity_type_name}/{stage_name}/{entity_id}/{filename}"

        # Decodificar contenido base64
        file_content = base64.b64decode(encoded)

        # Crear cliente S3
        s3 = boto3.client(
            "s3",
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        # Subir archivo
        s3.upload_fileobj(BytesIO(file_content), os.getenv("S3_BUCKET_NAME"), key)

        # URL del archivo
        file_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"

        print("Archivo subido a:", file_url)
        return file_url

    except Exception as e:
        print("Error al subir el archivo a S3:", e)
        raise e
