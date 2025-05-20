from modules.BudgetModule.models.o_budgets_status_changes import BudgetStatusChange
from modules.BudgetModule.schemas.budget_state_change_schema import OBudgetStatusChangeCreate, OBudgetStatusChangeUpdate
from modules.BudgetModule.repositories.budget_status_change_repository import BudgetStatusChangeRepository
from services.base_services import BaseService

class BudgetStatusChangeService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetStatusChangeRepository(db)
        super().__init__(
            BudgetStatusChange,
            self.repo,
            OBudgetStatusChangeCreate,
            OBudgetStatusChangeUpdate
        )
