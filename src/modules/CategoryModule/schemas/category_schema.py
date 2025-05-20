from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class MCategoryBase(BaseModel):
    name: str = Field(..., max_length=255, example="Category Name")

    @model_validator(mode="before")
    def name_validator(cls, values):
        name = values.get("name")
        if not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        return values

    class Config:
        from_attributes = True


class MCategoryCreate(MCategoryBase):
    pass


class MCategoryUpdate(MCategoryBase):
    name: Optional[str] = None
    region_id: Optional[int] = None

    @model_validator(mode="before")
    def name_update_validator(cls, values):
        name = values.get("name")
        if name is not None and not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        return values


class MCategoryResponse(MCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
