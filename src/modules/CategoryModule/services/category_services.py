from modules.CategoryModule.models.m_categories import MCategory
from modules.CategoryModule.services.category_region_services import CategoryRegionService
from modules.CategoryModule.schemas.category_schema import MCategoryCreate, MCategoryUpdate
from modules.CategoryModule.repositories.category_repository import CategoryRepository
from services.base_services import BaseService
from utils.serialize import serialize_model
class CategoryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repository = CategoryRepository(db)
        super().__init__(
            MCategory,
            self.repository,
            MCategoryCreate,
            MCategoryUpdate
        )


    def create_with_region(self, data):
        try:
            category = {
                "name": data['name']
            }
            
            data_response = []
            
            create_category = self.create(category)
            data_response.append(serialize_model(create_category))
            
            category_region = {
                "category_id": create_category.id,
                "region_id": data['region_id']
            }
            
            service = CategoryRegionService(self.db)
            
            create_relation = service.create(category_region)
            data_response.append(serialize_model(create_relation))
            
            return data_response
            
        except Exception as e:
            raise e