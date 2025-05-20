from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets_timeline import BudgetTimeline
from repositories.base_repository import BaseRepository

class  BudgetTimelineRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db,  BudgetTimeline)
