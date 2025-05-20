from pydantic import BaseModel, ConfigDict,model_validator
from typing import Optional
from datetime import datetime
from modules.CategoryModule.models.m_regions import MRegion
from modules.CategoryModule.models.m_categories import MCategory

class MCategoryRegionBase(BaseModel):
    region_id: int
    category_id: int
    data: Optional[dict] = None
    active: Optional[int] = 1

class MCategoryRegionCreate(MCategoryRegionBase):
    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        region_id = values.get('region_id')
        category_id = values.get('category_id')

        if region_id is not None:
            region = db.query(MRegion).filter(MRegion.id == region_id).first()
            if not region:
                raise Exception(f"No se encontró una region con id '{region_id}'.")

        if category_id is not None:
            category = db.query(MCategory).filter(MCategory.id == category_id).first()
            if not category:
                raise Exception("No se encontró categoría con el id " + {category_id})
                    
        return values

class MCategoryRegionUpdate(BaseModel):
    data: Optional[dict] = None
    active: Optional[int] = None

class MCategoryRegionOut(MCategoryRegionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)