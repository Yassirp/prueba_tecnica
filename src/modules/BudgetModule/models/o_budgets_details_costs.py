from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Numeric, func
from database.base import Base
from sqlalchemy.orm import relationship

class BudgetDetailCost(Base):
    __tablename__ = 'o_budgets_details_costs'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    budget_id = Column(Integer, ForeignKey('o_budgets.id'))
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    value = Column(Numeric)
    percentage = Column(Numeric)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    
    concept = relationship("MParameterValue", foreign_keys=[concept_id], lazy='select')
    type = relationship("MParameterValue", foreign_keys=[type_id], lazy='select')
    budget = relationship("OBudget", back_populates="budget_details", lazy='select')
    