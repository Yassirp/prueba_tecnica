from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey,  Date,func
from database.base import Base
from sqlalchemy.orm import relationship

class BudgetTimeline(Base):
    __tablename__ = 'o_budgets_timeline'

    id = Column(Integer, primary_key=True)
    budget_subcategory_id = Column(Integer, ForeignKey('o_budgets_subcategories.id'))
    start_date = Column(Integer)
    end_date = Column(Integer)
    status_id = Column(Integer, ForeignKey('m_object_states.id'))
    data = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    subcategory = relationship("BudgetSubcategory", back_populates="timeline")    