from pydantic import BaseModel
from decimal import Decimal



class BudgetQuantityTotalBase(BaseModel):
    budget_quantity_detail_id: int
    total: Decimal

class BudgetQuantityTotalCreate(BudgetQuantityTotalBase):
    pass

class BudgetQuantityTotalUpdate(BudgetQuantityTotalBase):
    pass

class BudgetQuantityTotalRead(BudgetQuantityTotalBase):
    id: int
    class Config:
        from_attributes = True