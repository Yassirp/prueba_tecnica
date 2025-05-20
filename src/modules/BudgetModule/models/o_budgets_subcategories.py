from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Numeric,func,Float
from database.base import Base
from sqlalchemy.orm import relationship

class BudgetSubcategory(Base):
    __tablename__ = 'o_budgets_subcategories'

    id = Column(Integer, primary_key=True)
    budget_category_id = Column(Integer, ForeignKey('o_budgets_categories.id'))
    subcategory_id = Column(Numeric, ForeignKey('m_subcategories.id') )
    total_value = Column(Float)
    total_quantity = Column(Float)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    
    subcategory = relationship("MSubCategory", foreign_keys=[subcategory_id], lazy='select')
    quantity_details = relationship(
        "OBudgetQuantityDetail",
        back_populates="budget_subcategory",
        cascade="all, delete-orphan",
        lazy="select"
    )
    category = relationship("BudgetCategory", back_populates="subcategories", lazy='select')
    timeline = relationship(
        "BudgetTimeline",
        back_populates="subcategory",  # nombre correcto en el otro modelo
        uselist=False,  # <--- esto hace que sea un solo objeto y no una lista
        lazy='select'
    )