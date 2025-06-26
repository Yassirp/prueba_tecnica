from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class CModuleActionBase(BaseModel):
    module_id: int = Field(..., example=1)
    action_id: int = Field(..., example=1)

    @model_validator(mode="before")
    def validate_positive_ids(cls, values):
        module_id = values.get("module_id")
        action_id = values.get("action_id")
        
        if module_id <= 0:
            raise Exception("The value for 'module_id' must be a positive integer.")
        
        if action_id <= 0:
            raise Exception("The value for 'action_id' must be a positive integer.")
        
        return values

    class Config:
        from_attributes = True


class CModuleActionCreate(CModuleActionBase):
    pass


class CModuleActionUpdate(CModuleActionBase):
    module_id: Optional[int] = None
    action_id: Optional[int] = None

    @model_validator(mode="before")
    def validate_optional_positive_ids(cls, values):
        module_id = values.get("module_id")
        action_id = values.get("action_id")
        
        if module_id is not None and module_id <= 0:
            raise Exception("The value for 'module_id' must be a positive integer.")
        
        if action_id is not None and action_id <= 0:
            raise Exception("The value for 'action_id' must be a positive integer.")
        
        return values


class CModuleActionResponse(CModuleActionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
