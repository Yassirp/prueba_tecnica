from modules.CategoryModule.models.m_subcategories import MSubCategory
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import  joinedload

class SubcategoryRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MSubCategory)


    def get_subcategory_by_apu(self, subcategory_apu):
         return self.db.query(MSubCategory).filter(MSubCategory.apu == subcategory_apu).first()


    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None):
        query = self.db.query(MSubCategory).options(
            joinedload(self.model.category),
            joinedload(self.model.subcategory_details)
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
        
        for subcategory in items:
            data = {
                    "id": subcategory.id,
                    "name": subcategory.name,
                    "total_value": subcategory.total_value,
                    "category": {
                        "id": subcategory.category.id,
                        "name": subcategory.category.name,
                        "region": {
                            "id": subcategory.category.region.id,
                            "name": subcategory.category.region.name,
                        }
                    },
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
                }
            results.append(data)
        
        return results, total
