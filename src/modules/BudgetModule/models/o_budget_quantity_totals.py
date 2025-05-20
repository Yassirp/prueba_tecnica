from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.base import Base


class OBudgetQuantityTotal(Base):
    __tablename__ = "o_budget_quantity_totals"

    id = Column(Integer, primary_key=True, index=True)
    budget_quantity_detail_id = Column(Integer, ForeignKey("o_budget_quantity_details.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    total = Column(DECIMAL(12, 2))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    detail = relationship("OBudgetQuantityDetail", back_populates="total")