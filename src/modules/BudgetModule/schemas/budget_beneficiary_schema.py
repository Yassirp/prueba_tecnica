from pydantic import BaseModel, Field, model_validator
from typing import Optional
from database.database import get_db
from modules.BudgetModule.models.o_budgets import  OBudget
from modules.FlowModule.models.m_object_states import MObjectState  

class OBudgetBeneficiaryCreate(BaseModel):
    beneficiary_id: int = Field(..., description="ID del beneficiario")
    budget_id: int = Field(..., description="ID del presupuesto asociado")
    status_id: int = Field(..., description="ID del estado")

    @model_validator(mode='before')
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)

        # Validar que budget_id exista
        budget_id = values.get('budget_id')
        if budget_id:
            exists_budget = db.query(OBudget).filter(OBudget.id == budget_id).first()
            if not exists_budget:
                raise Exception(f"El presupuesto con id '{budget_id}' no existe.")

        # Validar que status_id exista
        status_id = values.get('status_id')
        if status_id:
            exists_status = db.query(MObjectState).filter(MObjectState.id == status_id).first()
            if not exists_status:
                raise Exception(f"El estado con id '{status_id}' no existe.")

        return values

class OBudgetBeneficiaryUpdate(BaseModel):
    beneficiary_id: Optional[int] = Field(None, description="ID del beneficiario")
    status_id: Optional[int] = Field(None, description="ID del estado")

    @model_validator(mode='before')
    def validate_update_fields(cls, values: dict, info):
        db = info.context.get("db", None)

        status_id = values.get('status_id')
        if status_id:
            exists_status = db.query(MObjectState).filter(MObjectState.id == status_id).first()
            if not exists_status:
                raise Exception(f"El estado con id '{status_id}' no existe.")

        return values
