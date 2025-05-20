from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL, func
from database.base import Base
from sqlalchemy.orm import relationship

class MProduct(Base):
    __tablename__ = 'm_products'

    id = Column(Integer, primary_key=True)
    reference = Column(String)
    name = Column(String)
    unit_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    value = Column(DECIMAL)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    subcategory_details = relationship("MSubCategoryDetail", back_populates="product")
    unit_value = relationship("MParameterValue", back_populates="parent_product")