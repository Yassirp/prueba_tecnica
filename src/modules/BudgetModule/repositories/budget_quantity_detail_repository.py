from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budget_quantity_details import OBudgetQuantityDetail
from repositories.base_repository import BaseRepository

class BudgetQuantityDetailRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, OBudgetQuantityDetail)

