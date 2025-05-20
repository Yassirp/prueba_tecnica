from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL, func
from database.base import Base
from sqlalchemy.orm import relationship

class MSubCategory(Base):
    __tablename__ = 'm_subcategories'

    id = Column(Integer, primary_key=True)
    apu = Column(String)
    category_id = Column(Integer, ForeignKey('m_categories_regions.id'))  # ✅ Cambio aquí
    name = Column(String)
    unit= Column(String)
    total_value = Column(DECIMAL)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    subcategory_details = relationship("MSubCategoryDetail", back_populates="subcategory")
    # category_region_id = Column(Integer, ForeignKey('m_categories_regions.id'))  # asegúrate de que sea así
    category_region = relationship("MCategoryRegion", back_populates="subcategories")
