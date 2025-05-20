from modules.CategoryModule.models.m_subcategory_detail import MSubCategoryDetail
from repositories.base_repository import BaseRepository 

class SubcategoryDetailRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MSubCategoryDetail)

    def get_by_subcategory_id(self, subcategory_id):
        return self.db.query(MSubCategoryDetail).filter(MSubCategoryDetail.subcategory_id == subcategory_id).all()
    

    def get_by_product_category(self, subcategory_id, product_id):
        return self.db.query(MSubCategoryDetail).filter(
            MSubCategoryDetail.subcategory_id == subcategory_id,
            MSubCategoryDetail.product_id == product_id
        ).all()
        
    
    def get_stock(self, id):
        product = self.get_by_id(id)
        if product:
            return product.quantity
        return 0
    
    def save(self, sub_detail):
        self.db.add(sub_detail)
        self.db.commit()
        self.db.refresh(sub_detail)
        return sub_detail

    def delete(self, sub_detail):
        self.db.delete(sub_detail)
        self.db.commit()
