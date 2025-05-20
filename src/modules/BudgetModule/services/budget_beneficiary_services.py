from modules.BudgetModule.models.o_budgets_beneficiaries import BudgetBeneficiary
from modules.BudgetModule.schemas.budget_beneficiary_schema import OBudgetBeneficiaryCreate, OBudgetBeneficiaryUpdate
from modules.BudgetModule.repositories.budget_beneficiary_repository import BudgetBeneficiaryRepository
from services.base_services import BaseService

class BudgetBeneficiaryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetBeneficiaryRepository(db)
        super().__init__(
            BudgetBeneficiary,
            self.repo,
            OBudgetBeneficiaryCreate,
            OBudgetBeneficiaryUpdate
        )
        

