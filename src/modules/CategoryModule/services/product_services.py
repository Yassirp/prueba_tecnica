from modules.CategoryModule.models.m_products import MProduct
from modules.CategoryModule.repositories.product_repository import ProductRepository
from modules.CategoryModule.schemas.product_schema import MProductCreate, MProductUpdate
from services.base_services import BaseService 


class ProductService(BaseService):
    def __init__(self, db):
        self.repo = ProductRepository(db)
        super().__init__(MProduct, self.repo,MProductCreate, MProductUpdate)
