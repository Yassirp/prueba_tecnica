from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, DECIMAL, func
from database.base import Base
from sqlalchemy.orm import relationship

class MSubCategoryDetail(Base):
    __tablename__ = 'm_subcategories_details'

    id = Column(Integer, primary_key=True)
    subcategory_id = Column(Integer, ForeignKey('m_subcategories.id'))
    product_id = Column(Integer, ForeignKey('m_products.id'))
    quantity = Column(DECIMAL)
    unit_value = Column(DECIMAL)
    total_value = Column(DECIMAL)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    product = relationship("MProduct", back_populates="subcategory_details")
    subcategory = relationship("MSubCategory", back_populates="subcategory_details")