from modules.BudgetModule.models.o_budgets_categories import BudgetCategory
from modules.BudgetModule.schemas.budget_category_schema import OBudgetCategoryCreate, OBudgetCategoryUpdate
from modules.BudgetModule.repositories.budget_category_repository import BudgetCategoryRepository
from services.base_services import BaseService
from modules.CategoryModule.repositories.category_region_repository import CategoryRegionRepository
from utils.serialize import serialize_model
from modules.BudgetModule.services.budget_subcategory_services import BudgetSubcategoryService
from flask import   abort

class BudgetCategoryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetCategoryRepository(db)
        super().__init__(
            BudgetCategory,
            self.repo,
            OBudgetCategoryCreate,
            OBudgetCategoryUpdate
        )
        self.categories = CategoryRegionRepository(db)
        self.budget_subcategory_service = BudgetSubcategoryService(db)
        

    def create_budget_categories_with_subcategory(self, budget_id: int, categories: list[dict]):
        created_categories = []
        for detail in categories:
            find_category= self.categories.get_by_id(detail.get("id"))
            if not find_category:
                abort(404, description="category not found")

            category = self.create({
                "budget_id": budget_id,
                "category_id": find_category.id,
            })
            
            subcategories = self.budget_subcategory_service.create_budget_subcategories_with_product(category.id, detail.get("subcategories", []))
            created_categories.append({
                "category": serialize_model(category),
                "subcategories": subcategories
            })
        return created_categories


