from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory
from repositories.base_repository import BaseRepository

class  BudgetSubcategoryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetSubcategory)
