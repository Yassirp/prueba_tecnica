from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class CPermissionBase(BaseModel):
    associate_to: str = Field(..., example="User")
    associate_id: int = Field(..., example=1)
    action_id: int = Field(..., example=1)
    
    @model_validator(mode="before")
    def validate_associate_to(cls, values):
        associate_to = values.get("associate_to")
        if not associate_to:
            raise Exception("The 'associate_to' field must not be empty.")
        return values

    @model_validator(mode="before")
    def validate_associate_id(cls, values):
        associate_id = values.get("associate_id")
        if associate_id <= 0:
            raise Exception("The 'associate_id' must be a positive integer.")
        return values

    model_config = {
        "from_attributes": True
    }


class CPermissionCreate(CPermissionBase):
    pass


class CPermissionUpdate(CPermissionBase):
    associate_to: Optional[str] = None
    associate_id: Optional[int] = None
    action_id: Optional[int] = None

    @model_validator(mode="before")
    def validate_optional_associate_id(cls, values):
        associate_id = values.get("associate_id")
        if associate_id is not None and associate_id <= 0:
            raise Exception("The 'associate_id' must be a positive integer.")
        return values


class CPermissionResponse(CPermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
