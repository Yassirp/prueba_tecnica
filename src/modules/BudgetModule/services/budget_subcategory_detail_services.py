from modules.BudgetModule.models.o_budgets_subcategories_details import BudgetSubcategoryDetail
from modules.BudgetModule.schemas.budget_subcategory_detail_schema import OBudgetSubcategoryDetailCreate, OBudgetSubcategoryDetailUpdate
from modules.BudgetModule.repositories.budget_subcategory_detail_repository import BudgetSubcategoryDetailRepository
from services.base_services import BaseService
from utils.serialize import serialize_model
from flask import abort

from modules.CategoryModule.repositories.product_repository import ProductRepository
class BudgetSubcategoryDetailService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = BudgetSubcategoryDetailRepository(db)
        self.product = ProductRepository(db)
        super().__init__(
            BudgetSubcategoryDetail,
            self.repo,
            OBudgetSubcategoryDetailCreate,
            OBudgetSubcategoryDetailUpdate
        )
        
        
    def create_subcategory_details(self, subcategory_id: int, products: list[dict]):
        created_products = []
        for product in products:

            fin_product = self.product.get_by_id(product.get("product_id"))
            if not fin_product:
                abort(404, description="product not found")

            total_value = product.get("quantity") * float(fin_product.value)        
            detail = self.create({
                "budget_subcategory_id": subcategory_id,
                "product_id": product.get("product_id"),
                "quantity": product.get("quantity"),
                "total_value": total_value,
            })
            created_products.append(serialize_model(detail))
        return created_products