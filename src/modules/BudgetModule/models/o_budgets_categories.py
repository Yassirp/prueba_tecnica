from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String, func
from database.base import Base
from sqlalchemy.orm import relationship

class BudgetCategory(Base):
    __tablename__ = 'o_budgets_categories'

    id = Column(Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('o_budgets.id'))
    category_id = Column(Integer,ForeignKey('m_categories_regions.id'))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    
    categories_region = relationship("MCategoryRegion", foreign_keys=[category_id], lazy='select')
    subcategories = relationship("BudgetSubcategory", back_populates="category", lazy='select')
