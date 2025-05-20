from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budget_quantity_discounts import OBudgetQuantityDiscount
from repositories.base_repository import BaseRepository

class BudgetQuantityDiscountRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, OBudgetQuantityDiscount)

