# Archivo generado autom�ticamente para entity_document_logs - schemas
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema


class EntityDocumentLogBase(BaseModel):
    #entity_document_id: int = Field(..., ge=0, description="ID de la entidad documento")
    action: str = Field(..., max_length=200, description="Acción realizada")
    observations: Optional[str] = Field(None, max_length=200, description="Observaciones")
    before: Optional[dict] = Field(None, description="Datos antes de la acción")
    after: Optional[dict] = Field(None, description="Datos después de la acción")
    state: int = Field(1, ge=0, description="Estado activo (1) o inactivo (0)")


    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values

            #if "entity_document_id" not in values or values["entity_document_id"] is None:
             #   raise Exception("El ID de la entidad documento es requerido.")
            #elif not isinstance(values["entity_document_id"], int):
                #raise Exception("El ID de la entidad documento debe ser un número entero.")
            
            if "action" not in values or not values["action"] or not str(values["action"]).strip():
                raise Exception("La acción es requerida y no puede estar vacía.")
            elif not isinstance(values["action"], str):
                raise Exception("La acción debe ser una cadena de texto.")
            
            if "state" not in values or values["state"] is None:
                raise Exception("El estado es requerido.")
            elif not isinstance(values["state"], int):
                raise Exception("El estado debe ser un número entero.")
            

            return values
        except Exception as e:
            raise e
             
    
    
class EntityDocumentLogCreate(EntityDocumentLogBase):
    created_by: int = Field(..., ge=0, description="ID del usuario que creó el registro")


class EntityDocumentLogUpdate(EntityDocumentLogBase):
    #entity_document_id: int = Field(..., ge=0, description="ID de la entidad documento")
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