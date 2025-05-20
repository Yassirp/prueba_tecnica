from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budget_quantity_totals import OBudgetQuantityTotal
from repositories.base_repository import BaseRepository

class BudgetQuantityTotalRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, OBudgetQuantityTotal)

