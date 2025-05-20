from modules.CategoryModule.models.m_regions import MRegion
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import  joinedload
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
from modules.CategoryModule.models.m_subcategories import MSubCategory 
from modules.CategoryModule.models.m_subcategory_detail import MSubCategoryDetail

class RegionRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.model = MRegion
        super().__init__(self.db, self.model)



    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None):
        
        query = self.db.query(self.model).options(
            joinedload(self.model.categories)
            .joinedload(MCategoryRegion.subcategories)
            .joinedload(MSubCategory.subcategory_details)
        )
        
        if filters:
            query = self.filter_by(query, filters)

        if order_by:
            query = self.order_by(query, order_by)

        total = query.count()
        
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)


        items = query.all()
            
        results = []
        
        for item in items:
            data = {
                "id": item.id,
                "name": item.name,
                "categories": [
                    {
                        "id": category.id,
                        "name": category.name,
                        "subcategories": [
                            {
                                "id": subcategory.id,
                                "name": subcategory.name,
                                "total_value": subcategory.total_value,
                                "products": [
                                    {
                                        "name": subcategory_detail.product.name,
                                        "id" : subcategory_detail.product.id,
                                        "reference": subcategory_detail.product.reference,
                                        "quantity": subcategory_detail.quantity,
                                        "unit_id": subcategory_detail.product.unit_id,
                                        "value": subcategory_detail.product.value,
                                        "subcategory_detail_id": subcategory_detail.id,
                                    } for subcategory_detail in subcategory.subcategory_details
                                ]
                            } for subcategory in category.subcategories
                        ]
                    } for category in item.categories
                ]
            }
            
            results.append(data)
            
        return results, total
    
    
