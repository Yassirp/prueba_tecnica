from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_subcategories_details import BudgetSubcategoryDetail
from repositories.base_repository import BaseRepository

class  BudgetSubcategoryDetailRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetSubcategoryDetail)
