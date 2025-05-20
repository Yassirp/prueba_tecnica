import json
from datetime import datetime
from modules.CategoryModule.models.m_subcategory_detail import MSubCategoryDetail
from modules.CategoryModule.repositories.subcategory_detail_repository import SubcategoryDetailRepository
from modules.CategoryModule.repositories.product_repository import ProductRepository  
from modules.CategoryModule.repositories.subcategory_repository import SubcategoryRepository
from redis import Redis
from modules.CategoryModule.schemas.subcategory_detail_schema import MSubCategoryDetailCreate, MSubCategoryDetailUpdate
from services.base_services import BaseService


class SubcategoryDetailService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = SubcategoryDetailRepository(db)
        self.product_repo = ProductRepository(db)
        self.subcategory_repo = SubcategoryRepository(db)
        # self.redis = redis_client
        super().__init__(MSubCategoryDetail, self.repo,MSubCategoryDetailCreate, MSubCategoryDetailUpdate)

    def _check_quantity_threshold(self, sub_detail, user_name):
        product = self.product_repo.get_by_id(sub_detail.product_id)
        category_name =  self.subcategory_repo.get_by_id(sub_detail.subcategory_id).name
        used_quantity = sub_detail.quantity
        max_stock = self.repo.get_stock(sub_detail.product_id)

        if max_stock > 0 and used_quantity >= max_stock * 0.9:
            data = {
                "alert": "Cantidad supera el 90%",
                "category": category_name,
                "product": product.name,
                "used_by": user_name,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.redis.publish("inventory_alerts", json.dumps(data))
