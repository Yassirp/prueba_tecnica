from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from modules.ParameterModule.models.m_parameters_values import MParameterValue 
from modules.FlowModule.models.m_object_states import MObjectState

class OBudgetBase(BaseModel):
    code: str
    contractor_id: int
    contract_id: int
    department_id: int
    municipality_id: int
    beneficiary_id: int
    village: Optional[str] = None
    resolution_id: Optional[int] = None
    improvement_type_id: Optional[int] = None
    specific_improvement_id: Optional[int] = None
    valid_year: Optional[int] = None
    minimum_salary_id: Optional[int] = None
    presentation_date: Optional[date] = None
    scheme_type_id: Optional[int] = None
    legal_minimum_wages: Optional[int] = None
    subtotal_direct_costs: Optional[Decimal] = None
    subtotal_indirect_costs: Optional[Decimal] = None
    total_diagnosis: Optional[Decimal] = None
    total_budget: Optional[Decimal] = None
    status_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        for field in ['scheme_type_id', 'improvement_type_id', 'specific_improvement_id', 'status_id']:
            field_value = values.get(field)
            if field_value is not None:
                if field == 'scheme_type_id' or field == 'improvement_type_id' or field == 'specific_improvement_id':
                    exists = db.query(MParameterValue).filter(MParameterValue.id == field_value).first() is not None
                elif field == 'status_id':
                    exists = db.query(MObjectState).filter(MObjectState.id == field_value).first() is not None
                
                if not exists:
                    raise Exception(f"El valor para {field} no existe en la base de datos.")
        return values

    @model_validator(mode="before")
    def strip_strings(cls, values: dict) -> dict:
        for field in ('code', 'village'):
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()
        return values


class OBudgetCreate(OBudgetBase):
    code: str
    contractor_id: int
    contract_id: int
    department_id: int
    municipality_id: int
    improvement_type_id: int
    specific_improvement_id: Optional[int] = None
    minimum_salary_id: int
    scheme_type_id: int
    status_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @model_validator(mode="before")
    def strip_strings(cls, values: dict) -> dict:
        return super().strip_strings(values)


class OBudgetUpdate(BaseModel):
    code: Optional[str] = None
    contractor_id: Optional[int] = None
    contract_id: Optional[int] = None
    department_id: Optional[int] = None
    municipality_id: Optional[int] = None
    village: Optional[str] = None
    resolution_id: Optional[int] = None
    improvement_type_id: Optional[int] = None
    specific_improvement_id: Optional[int] = None
    valid_year: Optional[int] = None
    minimum_salary_id: Optional[int] = None
    presentation_date: Optional[date] = None
    scheme_type_id: Optional[int] = None
    legal_minimum_wages: Optional[int] = None
    subtotal_direct_costs: Optional[Decimal] = None
    subtotal_indirect_costs: Optional[Decimal] = None
    total_diagnosis: Optional[Decimal] = None
    total_budget: Optional[Decimal] = None
    status_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    
    
class OBudgetInDB(OBudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True