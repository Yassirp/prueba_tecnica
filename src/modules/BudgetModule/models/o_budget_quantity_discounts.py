from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey,TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.base import Base


class OBudgetQuantityDiscount(Base):
    __tablename__ = "o_budget_quantity_discounts"

    id = Column(Integer, primary_key=True, index=True)
    budget_quantity_detail_id = Column(Integer, ForeignKey("o_budget_quantity_details.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    element = Column(String(100))
    height = Column(DECIMAL(10, 2))
    width = Column(DECIMAL(10, 2))
    length = Column(DECIMAL(10, 2))
    quantity = Column(DECIMAL(10, 2))
    subtotal = Column(DECIMAL(12, 2))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    detail = relationship("OBudgetQuantityDetail", back_populates="discounts")