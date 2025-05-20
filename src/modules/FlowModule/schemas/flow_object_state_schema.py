from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime


class FlowObjectStateBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    flow_id: int
    object_state_id: int
    order_state: int
    role_assigned_id: Optional[str] = Field(None, min_length=1, max_length=100)
    user_assigned_id: Optional[str] = Field(None, min_length=1, max_length=100)

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for field in ('name', 'role_assigned_id', 'user_assigned_id'):
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()
        return values


class FlowObjectStateCreate(FlowObjectStateBase):
    pass


class FlowObjectStateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    flow_id: Optional[int] = None
    object_state_id: Optional[int] = None
    order_state: Optional[int] = None
    role_assigned_id: Optional[str] = Field(None, min_length=1, max_length=100)
    user_assigned_id: Optional[str] = Field(None, min_length=1, max_length=100)

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for field in ('name', 'role_assigned_id', 'user_assigned_id'):
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()
        return values


class FlowObjectStateInDB(FlowObjectStateBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True