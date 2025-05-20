from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class BudgetQuantityDiscountBase(BaseModel):
    budget_quantity_detail_id: int
    element: Optional[str]
    height: Optional[Decimal]
    width: Optional[Decimal]
    length: Optional[Decimal]
    quantity: Optional[Decimal]
    subtotal: Optional[Decimal]

class BudgetQuantityDiscountCreate(BudgetQuantityDiscountBase):
    pass

class BudgetQuantityDiscountUpdate(BudgetQuantityDiscountBase):
    pass

class BudgetQuantityDiscountRead(BudgetQuantityDiscountBase):
    id: int
    class Config:
        from_attributes = True