from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Numeric, func
from database.base import Base

class BudgetSubcategoryDetail(Base):
    __tablename__ = 'o_budgets_subcategories_details'

    id = Column(Integer, primary_key=True)
    budget_subcategory_id = Column(Integer, ForeignKey('o_budgets_subcategories.id'))
    product_id = Column(Integer, ForeignKey('m_products.id'))
    quantity = Column(Numeric)
    total_value = Column(Numeric)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    