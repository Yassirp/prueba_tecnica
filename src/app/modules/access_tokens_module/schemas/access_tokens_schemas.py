# Archivo generado automáticamente para access_tokens - schemas
from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema
from src.app.shared.constants.project_enum import Projectds

class AccessTokenBase(BaseModel):
    token: str = Field(max_length=100)
    state: int = Field(1,ge=0)
    project_id: int = Field(...,ge=0)

class AccessTokenOut(AccessTokenBase, BaseOutSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ValidateLogin(BaseModel):
    key: str = Field(...,description="Clave valor de la empresa a consultar.")
    project_id: int = Field(..., ge=0, description="Clave valor de la empresa a consultar.")
    municipality_id: Optional[int] = Field(None, description="Clave valor del municipio.")
    department_id: Optional[int] = Field(None, description="Clave valor del departamento.")
    region_id: Optional[int] = Field(None, description="Clave valor de la región.")
    user_id: Optional[int] = Field(None, description="Clave valor del usuario.")

    @root_validator(pre=True)
    def check_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not isinstance(values, dict):
                return values

            # Validación de `key`
            key = values.get("key")
            if key is None:
                raise Exception("La clave es requerida.")
            if not isinstance(key, str):
                raise Exception("La clave debe ser una cadena de texto.")
            if not key.strip():
                raise Exception("La clave no puede estar vacía o en blanco.")

            project_id = values.get("project_id")
            if project_id is None:
                raise Exception("La empresa asociada es requerida.")
            if not isinstance(project_id, int) or project_id < 1:
                raise Exception("El campo project_id debe ser un número entero positivo.")

            # Si el project_id es distinto de NAOWEE, validar campos adicionales
            if project_id != Projectds.NAOWEE.value:
                required_int_fields = [
                    ("municipality_id", "El municipio es requerido.", "El municipio debe ser un número entero positivo."),
                    ("department_id", "El departamento es requerido.", "El departamento debe ser un número entero positivo."),
                    ("region_id", "La región es requerida.", "La región debe ser un número entero positivo."),
                    ("user_id", "El usuario es requerido.", "El usuario debe ser un número entero positivo."),
                ]
                
                for field, msg_required, msg_invalid in required_int_fields:
                    if field not in values or values[field] is None:
                        raise Exception(msg_required)
                    
                    if not isinstance(values[field], int) or values[field] < 1:
                        raise Exception(msg_invalid)

            return values
        except Exception as e:
            raise e
        

class ValidateLogout(BaseModel):
    token: str = Field(...,description="Clave valor de la empresa a consultar.")


    @root_validator(pre=True)
    def check_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not isinstance(values, dict): return values

            token = values.get("token")
            if token is None:
                raise Exception("El token es requerido.")
            
            if not isinstance(token, str):
                raise Exception("El token debe ser una cadena de texto.")
            
            if not token.strip():
                raise Exception("El token no puede estar vacía o en blanco.")

            return values
        except Exception as e:
            raise e