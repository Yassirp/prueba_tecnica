from repositories.base_repository import BaseRepository
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
from modules.CategoryModule.models.m_subcategories import MSubCategory
from modules.CategoryModule.models.m_regions import MRegion
from modules.CategoryModule.models.m_categories import MCategory
from sqlalchemy.orm import joinedload, aliased
class CategoryRegionRepository(BaseRepository):
    def __init__(self, db):
        self.model = MCategoryRegion
        super().__init__(db, self.model)



    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None) -> list[MCategoryRegion]:
        query = self.db.query(self.model).options(
            joinedload(self.model.region),
            joinedload(self.model.category),
            joinedload(self.model.subcategories)
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
        
        regions_dict = {}

        for item in items:
            region_id = item.region.id

            if region_id not in regions_dict:
                regions_dict[region_id] = {
                    "id": region_id,
                    "name": item.region.name,
                    "categories": []
                }

            category_data = {
                "id": item.category.id,
                "name": item.category.name,
                "subcategories": [
                    {
                        "id": subcategory.id,
                        "name": subcategory.name,
                        "total_value": subcategory.total_value,
                        "products": [
                            {
                                "name": subcategory_detail.product.name,
                                "id": subcategory_detail.product.id,
                                "reference": subcategory_detail.product.reference,
                                "quantity": subcategory_detail.quantity,
                                "unit_id": subcategory_detail.product.unit_id,
                                "value": subcategory_detail.product.value,
                                "subcategory_detail_id": subcategory_detail.id,
                            } for subcategory_detail in subcategory.subcategory_details
                        ]
                    } for subcategory in item.subcategories
                ]
            }

            regions_dict[region_id]["categories"].append(category_data)

        # Convertimos a lista
        results = list(regions_dict.values())
            
        return results,total
    
    

    # def get_one_with_relationships(self, item_id: int, filters: dict =None):
    #     query = self.db.query(self.model, MSubCategory, MCategory,MRegion)

    #     # Joins explícitos
    #     query = query.join(MSubCategory, self.model.id == MSubCategory.category_id ) \
    #                 .join(MCategory, self.model.category_id == MCategory.id) \
    #                 .join(MRegion, self.model.region_id == MRegion.id) \
    #                 .filter(self.model.region_id == item_id)


    #     if filters:
    #         query = self.filter_by(query, filters)
            
    #     return query.first()
    
    def get_one_with_relationships(self, item_id: int, filters=None):
        query = self.db.query(
            self.model, MSubCategory, MCategory, MRegion
        ).join(
            MSubCategory, self.model.id == MSubCategory.category_id
        ).join(
            MCategory, self.model.category_id == MCategory.id
        ).join(
            MRegion, self.model.region_id == MRegion.id
        ).filter(
            self.model.region_id == item_id
        )

        if filters:
            apu_filter = filters.get("apu")
            if apu_filter:
                query = query.filter(MSubCategory.apu.like(f'{apu_filter}%'))

        return query.all()