from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_status_changes import BudgetStatusChange
from repositories.base_repository import BaseRepository

class  BudgetStatusChangeRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetStatusChange)
