from modules.CategoryModule.models.m_subcategories import MSubCategory
from modules.CategoryModule.repositories.subcategory_detail_repository import SubcategoryDetailRepository
from modules.CategoryModule.repositories.product_repository import ProductRepository    
from modules.CategoryModule.schemas.subcategory_schema import MSubCategoryCreate, MSubCategoryUpdate
from modules.CategoryModule.repositories.subcategory_repository import SubcategoryRepository
from services.base_services import BaseService

class SubcategoryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = SubcategoryRepository(db)
        super().__init__(MSubCategory, self.repo, MSubCategoryCreate, MSubCategoryUpdate)
        
        
    def get_subcategory_products(self, subcategory_apu):
        subcategory = self.repo.get_subcategory_by_apu(str(subcategory_apu))
        if not subcategory:
            raise Exception("Subcategory not found")

        subcategory_detail_repo = SubcategoryDetailRepository(self.db)
        product_repo = ProductRepository(self.db)

        subcategory_details = subcategory_detail_repo.get_by_subcategory_id(subcategory.id)
        if not subcategory_details:
            raise Exception("No products found for this subcategory")

        product_ids = [detail.product_id for detail in subcategory_details]

        products_data = product_repo.get_by_ids(product_ids)

        product_map = {product.id: product for product in products_data}

        products = [
            {
                "id": product.id,
                "reference": product.reference,
                "name": product.name,
                "price": product.value
            }
            for detail in subcategory_details
            if (product := product_map.get(detail.product_id))
        ]

        return {
            "id": subcategory.id,
            "name": subcategory.name,
            "apu": subcategory.apu,
            "products": products
        }
