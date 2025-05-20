from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, func, JSON
from database.base import Base
from sqlalchemy.orm import relationship

class MCategoryRegion(Base):
    __tablename__ = 'm_categories_regions'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    region_id = Column(Integer, ForeignKey('m_regions.id'))
    category_id = Column(Integer, ForeignKey('m_categories.id'))
    data = Column(JSON)
    active = Column(Integer)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    region = relationship("MRegion", back_populates="categories")
    category = relationship("MCategory", back_populates="categories_region")
    subcategories = relationship("MSubCategory", back_populates="category_region")

