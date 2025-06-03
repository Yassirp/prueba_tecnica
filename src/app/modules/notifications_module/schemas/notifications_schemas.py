# Archivo generado autom�ticamente para notifications - schemas
from pydantic import BaseModel, Field, root_validator
from typing import Optional 
from src.app.shared.bases.base_schema import BaseOutSchema      
from datetime import datetime



class NotificationBase(BaseModel):
    type_notification_id: int = Field(..., ge=0, description="ID de la notificación")
    entity_document_id: int = Field(..., ge=0, description="ID de la entidad documento")
    title: str = Field(..., max_length=255, description="Título de la notificación")
    message: str = Field(..., description="Mensaje de la notificación")
    data: Optional[dict] = Field(None, description="Datos adicionales de la notificación")
    link: Optional[str] = Field(None, description="Enlace de la notificación")
    is_read: bool = Field(False, description="Indica si la notificación ha sido leída")
    state: int = Field(1, ge=0, description="Estado de la notificación")


    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict):
                return values

            required_int_fields = [
                ("type_notification_id", "El ID de la notificación es requerido.", "El ID de la notificación debe ser un número entero positivo."),
                ("entity_document_id", "El ID de la entidad documento es requerido.", "El ID de la entidad documento debe ser un número entero positivo."),
                ("state", "El estado de la notificación es requerido.", "El estado de la notificación debe ser un número entero."),
            ]

            required_str_fields = [
                ("title", "El título de la notificación es requerido.", "El título de la notificación debe ser una cadena de texto."),
                ("message", "El mensaje de la notificación es requerido.", "El mensaje de la notificación debe ser una cadena de texto."),
            ]

            for field, msg_required, msg_invalid in required_int_fields:
                value = values.get(field)
                if value is None:
                    raise Exception(msg_required)
                if not isinstance(value, int) or (field != "state" and value <= 0):
                    raise Exception(msg_invalid)

            for field, msg_required, msg_invalid in required_str_fields:
                value = values.get(field)
                if not value or not str(value).strip():
                    raise Exception(msg_required)
                if not isinstance(value, str):
                    raise Exception(msg_invalid)

            return values

        except Exception as e:
            raise e
    

class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    type_notification_id: Optional[int] = Field(None, ge=0, description="ID de la notificación")
    entity_document_id: Optional[int] = Field(None, ge=0, description="ID de la entidad documento")
    title: Optional[str] = Field(None, max_length=255, description="Título de la notificación")
    message: Optional[str] = Field(None, description="Mensaje de la notificación")
    data: Optional[dict] = Field(None, description="Datos adicionales de la notificación")
    link: Optional[str] = Field(None, description="Enlace de la notificación")
    is_read: Optional[bool] = Field(None, description="Indica si la notificación ha sido leída")       
    state: Optional[int] = Field(None, ge=0, description="Estado de la notificación")

class NotificationOut(NotificationBase, BaseOutSchema):
    id: int = Field(..., ge=0, description="ID de la notificación")
    created_by: Optional[int] = Field(None, description="ID del usuario que creó la notificación")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación de la notificación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización de la notificación")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación de la notificación")




    
       
       
       
