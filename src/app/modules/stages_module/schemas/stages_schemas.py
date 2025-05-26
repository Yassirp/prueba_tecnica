from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, model_validator
from src.app.shared.bases.base_schema import BaseOutSchema

class StageBase(BaseModel):
    name: str                  = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    project_id: int            = Field(ge=1)

    @model_validator(mode='before')
    def validate_all(cls, values: Any) -> Any:
        try:
            # Solo validamos si values es un dict
            if not isinstance(values, dict): return values

            name = values.get('name')
            project_id = values.get('project_id')

            if name is None:
                raise Exception('El campo name es requerido.')
            
            if not isinstance(name, str):
                raise Exception('El campo name debe ser una cadena de texto.')

            if project_id is None:
                raise Exception('El campo project_id es requerido.')
            
            if not isinstance(project_id, int):
                raise Exception('El campo project_id debe ser un entero.')

            if project_id < 1:
                raise Exception('El campo project_id" debe ser mayor o igual a 1.')
            
            return values
        except Exception as e:
            raise e

        
       

class StageCreate(StageBase):
    pass

class StageUpdate(BaseModel):
    name: Optional[str]        = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=100)
    project_id: Optional[int]  = Field(None, ge=1)
    state: Optional[int]       = Field(None, ge=0)

class StageOut(StageBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
