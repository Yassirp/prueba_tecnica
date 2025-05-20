from modules.BudgetModule.models.o_budgets_timeline import BudgetTimeline
from modules.BudgetModule.schemas.budget_timeline_schema import OBudgetTimelineCreate, OBudgetTimelineUpdate
from modules.BudgetModule.repositories.budget_timeline_repository import BudgetTimelineRepository
from services.base_services import BaseService
from utils.serialize import serialize_model
class BudgetTimelineService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetTimelineRepository(db)
        super().__init__(
            BudgetTimeline,
            self.repo,
            OBudgetTimelineCreate,
            OBudgetTimelineUpdate
        )
        
        
    def create_massive(self, data: list):
        data_response=[]
        for item in data:
            i = self.create(item)
            data_response.append(serialize_model(i))
            
            
        return data_response
            
        
        