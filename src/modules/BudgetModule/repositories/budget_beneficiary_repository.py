from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_beneficiaries import BudgetBeneficiary
from repositories.base_repository import BaseRepository

class  BudgetBeneficiaryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetBeneficiary)
