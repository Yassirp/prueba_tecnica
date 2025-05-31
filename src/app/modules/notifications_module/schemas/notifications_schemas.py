# Archivo generado autom�ticamente para notifications - schemas
from pydantic import BaseModel, Field, root_validator
from typing import Optional 
from src.app.shared.bases.base_schema import BaseOutSchema      
from datetime import datetime



class NotificationBase(BaseModel):
    type_notification_id: int = Field(..., ge=0, description="ID de la notificación")
    title: str = Field(..., max_length=255, description="Título de la notificación")
    message: str = Field(..., description="Mensaje de la notificación")
    data: Optional[dict] = Field(None, description="Datos adicionales de la notificación")
    link: Optional[str] = Field(None, description="Enlace de la notificación")
    is_read: bool = Field(False, description="Indica si la notificación ha sido leída")
    state: int = Field(1, ge=0, description="Estado de la notificación")


    @root_validator(pre=True)
    def check_fields(cls, values):
        if not isinstance(values, dict): return values

        if "type_notification_id" not in values or values["type_notification_id"] is None:
            raise ValueError("El ID de la notificación es requerido")
        
        if "title" not in values or not values["title"] or not str(values["title"]).strip():
            raise ValueError("El título de la notificación es requerido")
        
        if "message" not in values or not values["message"] or not str(values["message"]).strip():
            raise ValueError("El mensaje de la notificación es requerido")
        
        if "state" not in values or values["state"] is None:
            raise ValueError("El estado de la notificación es requerido")
        
        return values
    

class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    type_notification_id: Optional[int] = Field(None, ge=0, description="ID de la notificación")
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




    
       
       
       
