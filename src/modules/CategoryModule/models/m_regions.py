# m_regions.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from database.base import Base

class MRegion(Base):
    __tablename__ = 'm_regions'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

# relación definida luego de todas las clases para evitar errores de carga
from sqlalchemy.orm import relationship
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
MRegion.categories = relationship("MCategoryRegion", back_populates="region")
