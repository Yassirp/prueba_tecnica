from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class MSubCategoryDetailBase(BaseModel):
    subcategory_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: Decimal = Field(..., example=100.50)
    unit_value: Decimal = Field(..., example=25.50)
    total_value: Decimal = Field(..., example=2550.00)
    @model_validator(mode="before")
    def validate_positive_values_update(cls, values):
        quantity = values.get('quantity')
        unit_value = values.get('unit_value')
        total_value = values.get('total_value')

        if quantity is not None:
            quantity = float(quantity)
            if quantity <= 0:
                raise Exception("The value for 'quantity' must be positive.")

        if unit_value is not None:
            unit_value = float(unit_value)
            if unit_value <= 0:
                raise Exception("The value for 'unit_value' must be positive.")

        if total_value is not None:
            total_value = float(total_value)
            if total_value <= 0:
                raise Exception("The value for 'total_value' must be positive.")

        return values
    class Config:
        from_attributes = True


class MSubCategoryDetailCreate(MSubCategoryDetailBase):
    
    pass


class MSubCategoryDetailUpdate(MSubCategoryDetailBase):
    subcategory_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[Decimal] = None
    unit_value: Optional[Decimal] = None
    total_value: Optional[Decimal] = None



class MSubCategoryDetailResponse(MSubCategoryDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
