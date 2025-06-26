from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class MModuleBase(BaseModel):
    level: Optional[int] = Field(..., example=1)
    name: str = Field(..., example="Module Name")
    path: Optional[str] = Field(None, example="/module/path")
    parent_id: Optional[int] = Field(None, example=1)
    active: bool = Field(..., example=True)
    position: Optional[int] = Field(None, example=1)
    icon: Optional[str] = Field(None, example="icon-path")
    
    @model_validator(mode="before")
    def validate_positive_ids(cls, values):
        level = values.get("level")
        position = values.get("position")
        
        if level is not None and level < 0:
            raise Exception("The value for 'level' must be a positive integer.")
        
        if position is not None and position < 0:
            raise Exception("The value for 'position' must be a positive integer.")
        
        return values

    class Config:
        from_attributes = True


class MModuleCreate(MModuleBase):
    pass


class MModuleUpdate(MModuleBase):
    level: Optional[int] = None
    name: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    active: Optional[bool] = None
    position: Optional[int] = None
    icon: Optional[str] = None

    @model_validator(mode="before")
    def validate_optional_positive_ids(cls, values):
        level = values.get("level")
        position = values.get("position")
        
        if level is not None and level < 0:
            raise Exception("The value for 'level' must be a positive integer.")
        
        if position is not None and position < 0:
            raise Exception("The value for 'position' must be a positive integer.")
        
        return values


class MModuleResponse(MModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
