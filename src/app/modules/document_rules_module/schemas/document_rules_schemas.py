# Archivo generado automáticamente para document_rules - schemas
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, ConfigDict
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
    
class DocumentRuleOut(DocumentRuleBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None