from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_categories import BudgetCategory
from repositories.base_repository import BaseRepository

class  BudgetCategoryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetCategory)
