from modules.CategoryModule.models.m_products import MProduct
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import  joinedload

class ProductRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MProduct)



    def get_stock(self, id):
        product = self.get_by_id(id)
        if product:
            return product.stock
        return 0
    
    def save(self, product):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product):
        self.db.delete(product)
        self.db.commit()

    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None):
        query = self.db.query(self.model).options(
            joinedload(self.model.unit_value)
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
                "name": item.name,
                "id" : item.id,
                "reference": item.reference,
                "unit_id": item.unit_id,
                "value": item.value,
                "unit":{
                    "id": item.unit_value.id,
                    "name": item.unit_value.value,
                    "description": item.unit_value.description,
                    "reference": item.unit_value.reference,
                }
            }
            results.append(data)
             
        return results, total
