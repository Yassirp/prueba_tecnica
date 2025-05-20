from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
class MSubCategoryBase(BaseModel):
    apu: Optional[str] = Field(None, max_length=255, example="A1234")
    category_id: int = Field(..., example=1)
    name: str = Field(..., max_length=255, example="SubCategory Name")
    total_value: Optional[Decimal] = Field(..., example=1000.50)

    @model_validator(mode="before")
    def validate_fields(cls, values):
        apu = values.get("apu")
        name = values.get("name")

        if apu is not None and not apu.strip():
            raise Exception("The 'apu' field cannot be empty.")
        if not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        
        return values

    class Config:
        from_attributes = True


class MSubCategoryCreate(MSubCategoryBase):
    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        category_id = values.get('category_id')
        if category_id is not None:
            category_id = db.query(MCategoryRegion).filter(MCategoryRegion.id == id).first()
            if not category_id:
                raise Exception(f"El category_id no fue encontrado '{category_id}'.")
        


class MSubCategoryUpdate(MSubCategoryBase):
    apu: Optional[str] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    total_value: Optional[Decimal] = None

    @model_validator(mode="before")
    def validate_optional_fields(cls, values):
        apu = values.get("apu")
        name = values.get("name")

        if apu is not None and not apu.strip():
            raise Exception("The 'apu' field cannot be empty.")
        if name is not None and not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        
        return values


class MSubCategoryResponse(MSubCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
