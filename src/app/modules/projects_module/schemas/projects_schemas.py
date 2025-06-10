from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field,root_validator
from src.app.shared.bases.base_schema import BaseOutSchema

class ProjectBase(BaseModel):
    name: str = Field(max_length=100)
    state: int = Field(1,ge=0)
    key: str = Field(..., description="Clave de la empresa.")
    

    @root_validator(pre=True)
    def check_fields(cls, values):
        try:
            if not isinstance(values, dict): return values

            # Validación del campo 'name'
            if "name" in values:
                if len(values["name"]) > 100:
                    raise Exception("El nombre no puede exceder los 100 caracteres.")
            else:
                raise Exception("El campo 'name' es obligatorio.")

            # Validación del campo 'key'
            if "key" in values:
                if len(values["key"]) > 200:
                    raise Exception("La clave no puede exceder los 200 caracteres.")
            else:
                raise Exception("El campo 'key' es obligatorio.")

            return values
        except Exception as e:
            raise e

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    state: Optional[int] = Field(None, ge=0)

class ProjectOut(ProjectBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
