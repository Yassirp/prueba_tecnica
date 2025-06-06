# Archivo generado automáticamente para access_tokens - schemas
from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema
from src.app.shared.constants.project_enum import Projectds

class AccessTokenBase(BaseModel):
    token: str = Field(max_length=100)
    state: int = Field(1,ge=0)
    project: int = Field(Projectds.COMITE.value,ge=0)

class AccessTokenOut(AccessTokenBase, BaseOutSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ValidateLogin(BaseModel):
    key: str = Field(...,description="Clave valor de la empresa a consultar.")


    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values
            key = values.get("key")

            if not isinstance(key, str):
                raise Exception("La clave debe ser una cadena de texto.")
    
            if not key.strip():
                raise Exception("La clave no puede estar vacío o en blanco.")

            return values
        except Exception as e:
            raise e