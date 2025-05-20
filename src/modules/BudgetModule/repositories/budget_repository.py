from sqlalchemy.orm import Session
from modules.BudgetModule.models.o_budgets import OBudget
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import joinedload
from modules.BudgetModule.models.o_budget_quantity_details import OBudgetQuantityDetail
from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory
from modules.BudgetModule.models.o_budgets_categories import BudgetCategory
class OBudgetRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, OBudget)


    def get_budget_by_beneficiary(self, beneficiary_id: int):
        return self.db.query(self.model).filter(self.model.beneficiary_id == beneficiary_id).first()


    def get_relationship_by_id(self, budget_id: int):
        return self.db.query(self.model)\
        .options(
            joinedload(self.model.improvement_type),
            joinedload(self.model.categories)
            .joinedload(BudgetCategory.subcategories)
            .joinedload(BudgetSubcategory.quantity_details),
            # joinedload(self.model.specific_improvement),
            joinedload(self.model.minimum_salary),
            joinedload(self.model.scheme_type),
            joinedload(self.model.status)
        )\
        .filter(self.model.id == budget_id)\
        .first()
        
        
        
    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None, user:dict = None) -> list:
        query = self.db.query(self.model)\
            .options(
                joinedload(self.model.improvement_type),
                joinedload(self.model.categories)
                .joinedload(BudgetCategory.subcategories)
                .joinedload(BudgetSubcategory.quantity_details),
                joinedload(self.model.minimum_salary),
                joinedload(self.model.scheme_type),
                joinedload(self.model.status)
            )\
                
                
        if user and getattr(user, "old_id", None) == 3:
            query = query.filter(self.model.contractor_id == getattr(user, "id", None))
            
        if filters:
            query =  self.filter_by(query, filters)

        if order_by:
           query = self.order_by(query, order_by)


        total = query.count()
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)


        items = query.all()        
        
        return items, total
        