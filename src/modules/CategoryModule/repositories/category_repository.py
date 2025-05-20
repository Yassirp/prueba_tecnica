from modules.CategoryModule.models.m_categories import MCategory
from sqlalchemy.orm import  joinedload
from repositories.base_repository import BaseRepository
from modules.CategoryModule.models.m_subcategories import MSubCategory
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
from modules.CategoryModule.models.m_subcategory_detail import MSubCategoryDetail

class CategoryRepository(BaseRepository):
    def __init__(self, db):
        self.model = MCategory
        super().__init__(db, self.model)



    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None) -> list[MCategory]:
        
        
        query = self.db.query(MCategory).options(
            joinedload(MCategory.categories_region)
                .joinedload(MCategoryRegion.region),
            joinedload(MCategory.categories_region)
                .joinedload(MCategoryRegion.subcategories)
                .joinedload(MSubCategory.subcategory_details)
                .joinedload(MSubCategoryDetail.product)
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
        
        for category in items:
            data = {
                "id": category.id,
                "name": category.name,
                "regions": [],
                "subcategories": []
            }

            for cr in category.categories_region:
                data["regions"].append({
                    "id": cr.region.id,
                    "name": cr.region.name,
                })

                for subcategory in cr.subcategories:
                    sub_data = {
                        "id": subcategory.id,
                        "name": subcategory.name,
                        "total_value": subcategory.total_value,
                        "products": [
                            {
                                "name": detail.product.name,
                                "id": detail.product.id,
                                "reference": detail.product.reference,
                                "quantity": detail.quantity,
                                "unit_id": detail.product.unit_id,
                                "value": detail.product.value,
                                "subcategory_detail_id": detail.id,
                            }
                            for detail in subcategory.subcategory_details
                        ]
                    }
                    data["subcategories"].append(sub_data)

            results.append(data)

            
        return results, total  