from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory
from modules.BudgetModule.schemas.budget_subcategory_schema import OBudgetSubcategoryCreate, OBudgetSubcategoryUpdate
from modules.BudgetModule.repositories.budget_subcategory_repository import BudgetSubcategoryRepository
from modules.BudgetModule.services.budget_quantity_detail_services import BudgetQuantityDetailService
from services.base_services import BaseService
from flask import abort
import math
from utils.serialize import serialize_model
from modules.BudgetModule.services.budget_subcategory_detail_services import BudgetSubcategoryDetailService
from modules.CategoryModule.repositories.subcategory_repository import SubcategoryRepository

class BudgetSubcategoryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetSubcategoryRepository(db)
        super().__init__(
            BudgetSubcategory,
            self.repo,
            OBudgetSubcategoryCreate,
            OBudgetSubcategoryUpdate
        )
        
        self.subcategory = SubcategoryRepository(db)
        self.budget_quantity_detail = BudgetQuantityDetailService(db)
        self.budget_subcategory_detail = BudgetSubcategoryDetailService(db)
        
        
    def create_budget_subcategories_with_product(self, category_id: int, subcategories: list[dict]):
        try:
            created_subcategories = []
            for data in subcategories:
                
                find_subcategory = self.subcategory.get_by_id(data.get("id"))
                if not find_subcategory:
                    abort(404, description="subcategory not found")


                total_value = data.get("total_quantity") * float(find_subcategory.total_value)
                subcategory_data = {
                    "budget_category_id": category_id,
                    "subcategory_id": find_subcategory.id,
                    "total_quantity": data.get("total_quantity"),
                    "total_value": math.ceil(total_value),
                }
                subcategory = self.create(subcategory_data)

                if data.get("products"):
                    products = self.budget_subcategory_detail.create_subcategory_details(
                        subcategory.id, data.get("products", [])
                    )
                    
                quantity_details = self.budget_quantity_detail.create_data( subcategory.id,data.get("quantity_details"))

                created_subcategories.append({
                    "subcategory": serialize_model(subcategory),
                    # "subcategory_products":products,
                    "quantity_details": quantity_details
                })
            return created_subcategories
        except Exception as e:
            raise e
        
        
    def update_budget_subcategories(self, budget_subcategories: list):
        pass
    