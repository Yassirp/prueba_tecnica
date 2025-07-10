from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from src.app.modules.parameters_module.schemas.parameter_values_schemas import ParameterValueOut
from src.app.modules.flow_module.schemas.object_state_schema import ObjectStateOut
from src.app.modules.user_module.schemas.user_base_schema import UserBase

class UserRelationshipBase(BaseModel):
    user_id: int = Field(..., description="ID del usuario principal.")
    user_relationship_id: int = Field(..., description="ID del usuario relacionado.")
    relationship_type_id: int = Field(..., description="Tipo de relación.")
    relationship_status_id: int = Field(default=0, description="Estado de la relación.") 

    @validator("user_relationship_id")
    def user_ids_must_be_different(cls, v, values):
        if "user_id" in values and values["user_id"] == v:
            raise ValueError("user_id y user_relationship_id no pueden ser iguales")
        return v

class SimpleUser(BaseModel):
    id: int
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    document_number: Optional[str] = None
    document_type_id: Optional[int] = None
    document_type: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserRelationshipCreate(UserRelationshipBase):
    pass

class UserRelationshipUpdate(BaseModel):
    user_id: Optional[int]
    user_relationship_id: Optional[int]
    relationship_status_id: Optional[int]
    relationship_type_id: Optional[int]
    @validator("user_relationship_id")
    def user_ids_must_be_different(cls, v, values):
        if "user_id" in values and values["user_id"] == v:
            raise ValueError("user_id y user_relationship_id no pueden ser iguales")
        return v



class UserRelationshipOut(UserRelationshipBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    model_config = {
        "from_attributes": True
    }

class UserRelationshipWithRelationshipOut(UserRelationshipBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    user_relationship: UserBase
    relationship_type: ParameterValueOut
    relationship_status: ObjectStateOut
    model_config = {
        "from_attributes": True
    }