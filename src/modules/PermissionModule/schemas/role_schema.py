from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class MRoleBase(BaseModel):
    code: str = Field(..., example="ROLE001")
    name: str = Field(..., example="Administrator")
    old_id: Optional[int] = None
    active: bool = Field(..., example=True)

    @model_validator(mode='before')
    def validate_fields(cls, values):
        code = values.get('code')
        name = values.get('name')
        old_id = values.get('old_id')

        if not code:
            raise Exception("The 'code' field must not be empty.")
        if not name:
            raise Exception("The 'name' field must not be empty.")
        if old_id is not None and old_id <= 0:
            raise Exception("The 'old_id' must be a positive integer.")
        
        return values

    class Config:
        from_attributes = True


class MRoleCreate(MRoleBase):
    pass


class MRoleUpdate(MRoleBase):
    code: Optional[str] = None
    name: Optional[str] = None
    old_id: Optional[int] = None
    active: Optional[bool] = None

    @model_validator(mode='before')
    def validate_optional_fields(cls, values):
        old_id = values.get('old_id')
        if old_id is not None and old_id <= 0:
            raise Exception("The 'old_id' must be a positive integer.")
        return values


class MRoleResponse(MRoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
