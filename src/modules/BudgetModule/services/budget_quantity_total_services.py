from services.base_services import BaseService
from sqlalchemy.orm import Session
from modules.BudgetModule.repositories.budget_quantity_total_repository import BudgetQuantityTotalRepository
from modules.BudgetModule.models.o_budget_quantity_totals import OBudgetQuantityTotal
from modules.BudgetModule.schemas.budget_quantity_total_schema import BudgetQuantityTotalCreate, BudgetQuantityTotalUpdate

class BudgetQuantityTotalService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.repository = BudgetQuantityTotalRepository(db)
        super().__init__(OBudgetQuantityTotal, self.repository, BudgetQuantityTotalCreate, BudgetQuantityTotalUpdate)

