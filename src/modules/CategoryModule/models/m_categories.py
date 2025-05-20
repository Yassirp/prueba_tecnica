from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from database.base import Base
from sqlalchemy.orm import relationship

class MCategory(Base):
    __tablename__ = 'm_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    # Usar cadenas para resolver la relación más tarde
    # subcategories = relationship("MSubCategory", back_populates="category")
    categories_region = relationship("MCategoryRegion", back_populates="category")
