# Archivo generado autom�ticamente para entity_document_logs - schemas
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema


class EntityDocumentLogBase(BaseModel):
    entity_document_id: int = Field(..., ge=0, description="ID de la entidad documento")
    action: str = Field(..., max_length=200, description="Acción realizada")
    observations: Optional[str] = Field(None, max_length=200, description="Observaciones")
    before: Optional[dict] = Field(None, description="Datos antes de la acción")
    after: Optional[dict] = Field(None, description="Datos después de la acción")
    state: int = Field(1, ge=0, description="Estado activo (1) o inactivo (0)")


    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict):
                return values

            required_int_fields = [
                ("entity_document_id", "El ID de la entidad documento es requerido.", "El ID de la entidad documento debe ser un número entero positivo."),
                ("state", "El estado es requerido.", "El estado debe ser un número entero."),
            ]

            required_str_fields = [
                ("action", "La acción es requerida y no puede estar vacía.", "La acción debe ser una cadena de texto."),
            ]

            for field, msg_required, msg_invalid in required_int_fields:
                value = values.get(field)
                if value is None:
                    raise ValueError(msg_required)
                if not isinstance(value, int) or value < 0:
                    raise ValueError(msg_invalid)

            for field, msg_required, msg_invalid in required_str_fields:
                value = values.get(field)
                if not value or not str(value).strip():
                    raise ValueError(msg_required)
                if not isinstance(value, str):
                    raise ValueError(msg_invalid)

            return values

        except Exception as e:
            raise e

             
    
    
class EntityDocumentLogCreate(EntityDocumentLogBase):
    created_by: int = Field(..., ge=0, description="ID del usuario que creó el registro")


class EntityDocumentLogUpdate(EntityDocumentLogBase):
    entity_document_id: int = Field(..., ge=0, description="ID de la entidad documento")
    action: Optional[str] = Field(None, max_length=200, description="Acción realizada")
    observations: Optional[str] = Field(None, max_length=200, description="Observaciones")
    before: Optional[dict] = Field(None, description="Datos antes de la acción")
    after: Optional[dict] = Field(None, description="Datos después de la acción")
    state: Optional[int] = Field(None, ge=0, description="Estado activo (1) o inactivo (0)")

class EntityDocumentLogOut(EntityDocumentLogBase, BaseOutSchema):
    id: int = Field(..., ge=0, description="ID de la entidad documento")
    created_by: Optional[int] = Field(None, description="ID del usuario que creó el registro")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None