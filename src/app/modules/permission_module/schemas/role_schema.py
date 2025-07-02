from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class MRoleBase(BaseModel):
    code: str = Field(..., description="Código del rol")
    name: str = Field(..., description="Nombre del rol")
    active: bool = Field(..., description="Estado del rol")

    @model_validator(mode='before')
    def validate_fields(cls, values):
        code = values.get('code')
        name = values.get('name')

        if not code:
            raise Exception("The 'code' field must not be empty.")
        if not name:
            raise Exception("The 'name' field must not be empty.")
        
        return values

    class Config:
        from_attributes = True


class MRoleCreate(MRoleBase):
    pass


class MRoleUpdate(MRoleBase):
    code: Optional[str] = None
    name: Optional[str] = None
    active: Optional[bool] = None

    @model_validator(mode='before')
    def validate_optional_fields(cls, values):
        return values


class MRoleResponse(MRoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoleOut(MRoleBase):  
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

