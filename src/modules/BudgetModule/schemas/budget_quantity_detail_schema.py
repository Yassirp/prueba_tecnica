from pydantic import BaseModel,model_validator
from decimal import Decimal
from typing import Optional
from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory
class BudgetQuantityDetailBase(BaseModel):
    budget_subcategory_id: int
    location: Optional[str]
    height: Optional[Decimal]
    width: Optional[Decimal]
    length: Optional[Decimal]
    quantity: Optional[Decimal]
    subtotal: Optional[Decimal]

class BudgetQuantityDetailCreate(BudgetQuantityDetailBase):
    pass
    # @model_validator(mode="before")
    # def validate_foreign_keys(cls, values: dict, info):
    #     db = info.context.get("db", None)
    #     budget_subcategory_id = values.get('budget_subcategory_id')
    #     if budget_subcategory_id:
    #         budget_subcategory = db.query(BudgetSubcategory).filter(BudgetSubcategory.id == budget_subcategory_id).first()
    #         if not budget_subcategory:
    #             raise Exception(f"La subcategoría con  id '{budget_subcategory_id}' no existe.")


class BudgetQuantityDetailUpdate(BudgetQuantityDetailBase):
    pass



class BudgetQuantityDetailRead(BudgetQuantityDetailBase):
    pass

    class Config:
        from_attributes = True