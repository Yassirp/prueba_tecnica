from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey, DECIMAL,func
from database.base import Base
from sqlalchemy.orm import relationship

class OBudget(Base):
    __tablename__ = 'o_budgets'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    contractor_id = Column(Integer)
    contract_id = Column(Integer)
    department_id = Column(Integer)
    beneficiary_id = Column(Integer)
    municipality_id = Column(Integer)
    village = Column(String)
    resolution_id = Column(Integer)
    improvement_type_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    specific_improvement_id = Column(String)
    valid_year = Column(Integer)
    minimum_salary_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    presentation_date = Column(Date)
    scheme_type_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    legal_minimum_wages = Column(Integer)
    subtotal_direct_costs = Column(DECIMAL)
    subtotal_indirect_costs = Column(DECIMAL)
    total_diagnosis = Column(DECIMAL)
    total_budget = Column(DECIMAL)
    status_id = Column(Integer, ForeignKey('m_object_states.id'))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
        # Relaciones con carga perezosa (lazy='select')
    improvement_type = relationship("MParameterValue", foreign_keys=[improvement_type_id], lazy='select')
    # specific_improvement = relationship("MParameterValue", foreign_keys=[specific_improvement_id], lazy='select')
    minimum_salary = relationship("MParameterValue", foreign_keys=[minimum_salary_id], lazy='select')
    scheme_type = relationship("MParameterValue", foreign_keys=[scheme_type_id], lazy='select')
    # budget_details = relationship("BudgetDetailCost", foreign_keys=[scheme_type_id], lazy='select')
    status = relationship("MObjectState", foreign_keys=[status_id], lazy='select')
    categories = relationship("BudgetCategory", backref="budget", lazy='select')
    observations = relationship("BudgetStatusChange", back_populates="budget", lazy='select')
    budget_details = relationship("BudgetDetailCost", back_populates="budget", lazy='select')
