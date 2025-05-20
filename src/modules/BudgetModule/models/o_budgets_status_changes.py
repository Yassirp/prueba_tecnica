from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Numeric, String,func
from database.base import Base
from sqlalchemy.orm import relationship

class BudgetStatusChange(Base):
    __tablename__ = 'o_budgets_status_changes'

    id = Column(Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('o_budgets.id'))
    status_id = Column(Integer, ForeignKey('m_object_states.id'))
    type_id= Column(Integer, ForeignKey('m_parameters_values.id'))
    user_id = Column(Numeric)
    observations = Column(String)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    budget = relationship("OBudget", back_populates="observations", lazy='select')
    status = relationship("MObjectState", foreign_keys=[status_id], lazy='select')
    type = relationship("MParameterValue", foreign_keys=[type_id], lazy='select')
    