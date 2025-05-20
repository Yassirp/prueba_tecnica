from modules.BudgetModule.models.o_budgets_details_costs import BudgetDetailCost
from modules.BudgetModule.schemas.budget_detail_const_schema import OBudgetDetailCostCreate, OBudgetDetailCostUpdate
from modules.BudgetModule.repositories.budget_detail_cost_repository import BudgetDetailCostRepository
from services.base_services import BaseService
import math
from utils.serialize import serialize_model
class BudgetDetailCostService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetDetailCostRepository(db)
        super().__init__(
            BudgetDetailCost,
            self.repo,
            OBudgetDetailCostCreate,
            OBudgetDetailCostUpdate
        )
        
        
    def create_budget_cost_details(self, budget_id, details):
        created_costs = []
        for detail in details:
            cost = self.create({
                "budget_id": budget_id,
                "type_id": detail.get("type_id"), 
                "concept_id": detail.get("concept_id"), 
                "value": math.ceil(detail.get("value")), 
                "percentage": detail.get("percentage")
            })
            created_costs.append(serialize_model(cost))
        return created_costs