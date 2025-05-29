# Archivo generado automáticamente para document_rules - schemas
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema

class DocumentRuleBase(BaseModel):
    name: str = Field(..., max_length=100, description="Nombre del parámetro")
    project_id: int = Field(..., ge=0, description="ID del proyecto")
    document_type_id: int = Field(..., ge=0, description="ID del tipo de documento") 
    entity_type_id: int = Field(..., ge=0, description="ID del tipo de entidad")
    stage_id: int = Field(..., ge=0, description="ID de la etapa")
    description: Optional[str] = Field(None, max_length=200, description="Descripción del parámetro")
    allowed_file_type: Optional[Union[List[str], dict]] = Field(None, description="Tipos de archivos permitidos (JSON)")
    is_required: bool = Field(False, description="¿Es requerido?")
    max_file_size: Optional[int] = Field(None, ge=0, description="Tamaño máximo del archivo en MB")
    state: int = Field(1, ge=0, description="Estado activo (1) o inactivo (0)")
    
    
    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values

            if "name" not in values or not values["name"] or not str(values["name"]).strip():
                raise Exception("El nombre de la regla es requerida y no puede estar vacía.")
            elif not isinstance(values["name"], str):
                raise Exception("El nombre de la regla debe ser una cadena de texto.")
            
            elif not isinstance(values["project_id"], int) or values["project_id"] < 0:
                raise Exception("El poyecto debe ser un número entero positivo.")
            elif "project_id" not in values or values["project_id"] is None:
                raise Exception("El poyecto es requerido.")
            elif not isinstance(values["project_id"], int) or values["project_id"] < 0:
                raise Exception("El poyecto debe ser un número entero positivo.")

            elif "document_type_id" not in values or values["document_type_id"] is None:
                raise Exception("El tipo de documento es requerido.")
            elif not isinstance(values["document_type_id"], int) or values["document_type_id"] < 0:
                raise Exception("El tipo de documento debe ser un número entero positivo.")

            elif "entity_type_id" not in values or values["entity_type_id"] is None:
                raise Exception("El tipo de entidad es requerido.")
            elif not isinstance(values["entity_type_id"], int) or values["entity_type_id"] < 0:
                raise Exception("El tipo de entidad debe ser un número entero positivo.")

            elif "stage_id" not in values or values["stage_id"] is None:
                raise Exception("El tipo de etapa es requerido.")
            elif not isinstance(values["stage_id"], int) or values["stage_id"] < 0:
                raise Exception("El tipo de etapa debe ser un número entero positivo.")

            if "max_file_size" in values and values["max_file_size"] is not None:
                if not isinstance(values["max_file_size"], int) or values["max_file_size"] < 0:
                    raise Exception("El tamaño del archivo debe ser un número entero positivo.")
        
            return values
        except Exception as e:
            raise e
       
    
class DocumentRuleCreate(DocumentRuleBase):
    pass


class DocumentRuleUpdate(BaseModel):
    name: str = Field(..., max_length=100, description="Nombre del parámetro")
    project_id: int = Field(..., ge=0, description="ID del proyecto")
    document_type_id: int = Field(..., ge=0, description="ID del tipo de documento") 
    entity_type_id: int = Field(..., ge=0, description="ID del tipo de entidad")
    stage_id: int = Field(..., ge=0, description="ID de la etapa")
    description: Optional[str] = Field(None, max_length=200, description="Descripción del parámetro")
    allowed_file_type: Optional[Union[List[str], dict]] = Field(None, description="Tipos de archivos permitidos (JSON)")
    is_required: bool = Field(False, description="¿Es requerido?")
    max_file_size: Optional[int] = Field(None, ge=0, description="Tamaño máximo del archivo en MB")
    state: int = Field(1, ge=0, description="Estado activo (1) o inactivo (0)")


    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values

            if "name" not in values or not values["name"] or not str(values["name"]).strip():
                raise Exception("El nombre de la regla es requerida y no puede estar vacía.")
            elif not isinstance(values["name"], str):
                raise Exception("El nombre de la regla debe ser una cadena de texto.")
            
            elif not isinstance(values["project_id"], int) or values["project_id"] < 0:
                raise Exception("El poyecto debe ser un número entero positivo.")
            elif "project_id" not in values or values["project_id"] is None:
                raise Exception("El poyecto es requerido.")
            elif not isinstance(values["project_id"], int) or values["project_id"] < 0:
                raise Exception("El poyecto debe ser un número entero positivo.")

            elif "document_type_id" not in values or values["document_type_id"] is None:
                raise Exception("El tipo de documento es requerido.")
            elif not isinstance(values["document_type_id"], int) or values["document_type_id"] < 0:
                raise Exception("El tipo de documento debe ser un número entero positivo.")

            elif "entity_type_id" not in values or values["entity_type_id"] is None:
                raise Exception("El tipo de entidad es requerido.")
            elif not isinstance(values["entity_type_id"], int) or values["entity_type_id"] < 0:
                raise Exception("El tipo de entidad debe ser un número entero positivo.")

            elif "stage_id" not in values or values["stage_id"] is None:
                raise Exception("El tipo de etapa es requerido.")
            elif not isinstance(values["stage_id"], int) or values["stage_id"] < 0:
                raise Exception("El tipo de etapa debe ser un número entero positivo.")

            if "max_file_size" in values and values["max_file_size"] is not None:
                if not isinstance(values["max_file_size"], int) or values["max_file_size"] < 0:
                    raise Exception("El tamaño del archivo debe ser un número entero positivo.")
        
            return values
        except Exception as e:
            raise e
    
class DocumentRuleOut(DocumentRuleBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None