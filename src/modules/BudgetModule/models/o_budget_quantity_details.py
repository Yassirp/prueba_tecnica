from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey,TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.base import Base



class OBudgetQuantityDetail(Base):
    __tablename__ = "o_budget_quantity_details"

    id = Column(Integer, primary_key=True, index=True)
    budget_subcategory_id = Column(Integer, ForeignKey("o_budgets_subcategories.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    location = Column(String(100))
    height = Column(DECIMAL(10, 2))
    width = Column(DECIMAL(10, 2))
    length = Column(DECIMAL(10, 2))
    quantity = Column(DECIMAL(10, 2))
    subtotal = Column(DECIMAL(12, 2))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    discounts = relationship("OBudgetQuantityDiscount", back_populates="detail", cascade="all, delete-orphan")
    total = relationship("OBudgetQuantityTotal", back_populates="detail", uselist=False, cascade="all, delete-orphan")
    budget_subcategory = relationship(
        "BudgetSubcategory",
        back_populates="quantity_details",
        lazy="select"
    )