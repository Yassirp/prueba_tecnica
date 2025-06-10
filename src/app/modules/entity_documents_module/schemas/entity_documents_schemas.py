# Archivo generado automáticamente para entity_documents - schemas
from datetime import datetime
import json
from fastapi import HTTPException, status
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, root_validator
from src.app.shared.bases.base_schema import BaseOutSchema
from src.app.shared.constants.attribute_and_parameter_enum import AttributeIds

class EntityDocumentBase(BaseModel):
    project_id: int = Field(..., ge=1, description="ID del proyecto (obligatorio)")
    document_type_id: int = Field(..., ge=1, description="ID del tipo de documento")
    entity_type_id: int = Field(..., ge=1, description="ID del tipo de entidad")
    entity_id: int = Field(..., ge=1, description="ID de la entidad externa (opcional)")
    stage_id: int = Field(..., ge=1, description="ID de la etapa")
    file_url: str = Field(..., description="Ruta del archivo en S3")
    file_extension: str = Field(..., max_length=100, description="Extensión del archivo")
    file_size: int = Field(..., ge=0, description="Tamaño del archivo en bytes")
    mime_type: int = Field(..., ge=0, description="Tipo MIME del archivo")
    upload_device: str = Field(..., max_length=100, description="Nombre del dispositivo desde el que se subió")
    upload_ip: str = Field(..., max_length=100, description="IP del dispositivo")
    document_status_id: int = Field(AttributeIds.PENDING_APPROVAL.value, ge=1, description="ID del estado del documento")
    observations: str = Field(..., max_length=100, description="Observaciones")
    state: int = Field(1,ge=0)
    properties: Optional[dict] = Field(None, description="Propiedaes por la cules filtrar.")
    properties_project: Optional[dict] =  Field(None, description="Data del projecto compratida.")

    # Campos adicionales que no se guardan en la base de datos
    email: Optional[str] = Field(None, description="Correo electrónico del usuario")
    name: Optional[str] = Field(None, description="Nombre del usuario")
    created_by: Optional[int] = Field(None, description="ID del usuario")
    class Config:
        extra = "allow"  # Permite campos extra
        exclude = {'email', 'name', 'created_by'}  # Excluye estos campos al serializar

    def dict_for_db(self) -> Dict[str, Any]:
        """Retorna un diccionario con solo los campos que van a la base de datos"""
        return self.model_dump(exclude={'email', 'name', 'created_by'})

    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values   

            required_int_fields = [
                ("project_id", "El proyecto es requerido.", "El proyecto debe ser un número entero positivo."),
                ("document_type_id", "El tipo de documento es requerido.", "El tipo de documento debe ser un número entero positivo."),
                ("entity_type_id", "El tipo de entidad es requerido.", "El tipo de entidad debe ser un número entero positivo."),
                ("entity_id", "La entidad externa es requerida.", "La entidad externa debe ser un número entero positivo."),
                ("stage_id", "La etapa es requerida.", "La etapa debe ser un número entero positivo."),
                ("file_size", "El tamaño del archivo es requerido.", "El tamaño del archivo debe ser un número entero positivo."),
                ("mime_type", "El tipo MIME es requerido.", "El tipo MIME debe ser un número entero positivo."),
                ("created_by", "El ID del usuario es requerido.", "El ID del usuario debe ser un número entero positivo."),
            ]   

            required_str_fields = [
                ("file_url", "La ruta del archivo es requerida.", "La ruta del archivo debe ser una cadena de texto."),
                ("file_extension", "La extensión del archivo es requerida.", "La extensión del archivo debe ser una cadena de texto."),
                ("upload_device", "El nombre del dispositivo es requerido.", "El nombre del dispositivo debe ser una cadena de texto."),
                ("upload_ip", "La IP del dispositivo es requerida.", "La IP del dispositivo debe ser una cadena de texto."),
                ("observations", "Las observaciones son requeridas.", "Las observaciones deben ser una cadena de texto."),
                ("email", "El email del usuario es requerido.", "El email del usuario debe ser una cadena de texto."),
                ("name", "El nombre del usuario es requerido.", "El nombre del usuario debe ser una cadena de texto."),
            ]   
            json_fields = [
                ("properties", "El campo properties es requerido y debe ser un JSON válido."),
                ("properties_project", "El campo properties_project es requerido y debe ser un JSON válido."),
            ]

            for field, msg_required, msg_invalid in required_int_fields:
                if field not in values or values[field] is None:
                    raise Exception(msg_required)
                if not isinstance(values[field], int) or values[field] < 0:
                    raise Exception(msg_invalid)    

            for field, msg_required, msg_invalid in required_str_fields:
                if field not in values or values[field] is None or not str(values[field]).strip():
                    raise Exception(msg_required)
                if not isinstance(values[field], str):
                    raise Exception(msg_invalid)    
                
            # Validar campos JSON requeridos
            for field, msg in json_fields:
                if field not in values or values[field] is None:
                    raise Exception(msg)
                # Comprobar que sea dict (JSON parseado)
                # Si viene como string, intentar parsear a dict
                val = values[field]
                if not isinstance(val, dict):
                    raise Exception(f"El campo {field} debe ser un JSON válido.")
                # Reasignar el valor parseado (por si viene como string JSON)
                values[field] = val
                    
            return values   

        except Exception as e:
            raise e

    
class EntityDocumentCreate(EntityDocumentBase):
    pass


class EntityDocumentUpdate(BaseModel):
    project_id: int = Field(..., ge=1, description="ID del proyecto (obligatorio)")
    document_type_id: int = Field(..., ge=1, description="ID del tipo de documento")
    entity_type_id: int = Field(..., ge=1, description="ID del tipo de entidad")
    entity_id: int = Field(..., ge=1, description="ID de la entidad externa (opcional)")
    stage_id: int = Field(..., ge=1, description="ID de la etapa")
    file_url: str = Field(..., description="Ruta del archivo en S3")
    file_extension: str = Field(..., max_length=100, description="Extensión del archivo")
    file_size: int = Field(..., ge=0, description="Tamaño del archivo en bytes")
    mime_type: int = Field(..., ge=0, description="Tipo MIME del archivo")
    upload_device: str = Field(..., max_length=100, description="Nombre del dispositivo desde el que se subió")
    upload_ip: str = Field(..., max_length=100, description="IP del dispositivo")
    document_status_id: int = Field(AttributeIds.PENDING_APPROVAL.value, ge=1, description="ID del estado del documento")
    observations: str = Field(..., max_length=100, description="Observaciones")
    created_by: int = Field(..., ge=1, description="ID del usuario")
    
    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values   

            required_int_fields = [
                ("project_id", "El proyecto es requerido.", "El proyecto debe ser un número entero positivo."),
                ("document_type_id", "El tipo de documento es requerido.", "El tipo de documento debe ser un número entero positivo."),
                ("entity_type_id", "El tipo de entidad es requerido.", "El tipo de entidad debe ser un número entero positivo."),
                ("entity_id", "La entidad externa es requerida.", "La entidad externa debe ser un número entero positivo."),
                ("stage_id", "La etapa es requerida.", "La etapa debe ser un número entero positivo."),
                ("file_size", "El tamaño del archivo es requerido.", "El tamaño del archivo debe ser un número entero positivo."),
                ("mime_type", "El tipo MIME es requerido.", "El tipo MIME debe ser un número entero positivo."),
                ("created_by", "El ID del usuario es requerido.", "El ID del usuario debe ser un número entero positivo."),
            ]   

            required_str_fields = [
                ("file_url", "La ruta del archivo es requerida.", "La ruta del archivo debe ser una cadena de texto."),
                ("file_extension", "La extensión del archivo es requerida.", "La extensión del archivo debe ser una cadena de texto."),
                ("upload_device", "El nombre del dispositivo es requerido.", "El nombre del dispositivo debe ser una cadena de texto."),
                ("upload_ip", "La IP del dispositivo es requerida.", "La IP del dispositivo debe ser una cadena de texto."),
                ("observations", "Las observaciones son requeridas.", "Las observaciones deben ser una cadena de texto."),
            ]   

            for field, msg_required, msg_invalid in required_int_fields:
                if field not in values or values[field] is None:
                    raise Exception(msg_required)
                if not isinstance(values[field], int) or values[field] < 0:
                    raise Exception(msg_invalid)    

            for field, msg_required, msg_invalid in required_str_fields:
                if field not in values or values[field] is None or not str(values[field]).strip():
                    raise Exception(msg_required)
                if not isinstance(values[field], str):
                    raise Exception(msg_invalid)    

            return values   

        except Exception as e:
            raise e


class EntityDocumentOut(EntityDocumentBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class EntityDocumentStatus(BaseModel):
    document_status_id: int = Field(..., ge=1, description="ID del estado del documento")
    documents: Any = Field(..., description="Lista de documentos")  # Aquí usamos Any para forzar la validación manual
    class Config:
        extra = "ignore" 

        
    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values

            required_int_fields = [
                ("document_status_id", "El estado del documento es requerido.", "El estado del documento debe ser un número entero positivo."),
            ]

            for field, msg_required, msg_invalid in required_int_fields:
                if field not in values or values[field] is None:
                    raise Exception(msg_required)
                
                if not isinstance(values[field], int) or values[field] < 1:
                    raise Exception(msg_invalid)
                
            documents = values.get("documents")
            if documents is None:
                raise Exception("El campo documents es requerido.")
            
            if not isinstance(documents, list):
                raise Exception("El campo documents debe ser un arreglo (array).")
            
            if len(documents) == 0:
                raise Exception("El campo documents no puede estar vacío.")
            
            return values
        except Exception as e:
            raise e