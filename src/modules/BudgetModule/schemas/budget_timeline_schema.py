from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory  
from modules.BudgetModule.models.o_budgets_beneficiaries import BudgetBeneficiary  
from modules.FlowModule.models.m_object_states import MObjectState  

class OBudgetTimelineCreate(BaseModel):
    budget_subcategory_id: int = Field(..., description="ID de la subcategoría del presupuesto")
    # budget_beneficiary_id: int = Field(..., description="ID del beneficiario del presupuesto")
    start_date: int = Field(..., description="Fecha de inicio del presupuesto")
    end_date: int = Field(..., description="Fecha de finalización del presupuesto")
    status_id: int = Field(..., description="ID del estado del presupuesto")
    data: Optional[date] = Field(None, description="Fecha de creación de los datos")

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        budget_subcategory_id = values.get('budget_subcategory_id')
        status_id = values.get('status_id')

        if budget_subcategory_id is not None:
            subcategory = db.query(BudgetSubcategory).filter(BudgetSubcategory.id == budget_subcategory_id).first()
            if not subcategory:
                raise Exception(f"No se encontró una subcategoría de presupuesto con id '{budget_subcategory_id}'.")

        if status_id is not None:
            status = db.query(MObjectState).filter(MObjectState.id == status_id).first()
            if not status:
                raise Exception(f"No se encontró un estado con id '{status_id}'.")
                    
        return values

class OBudgetTimelineUpdate(BaseModel):
    start_date: Optional[date] = Field(None, description="Fecha de inicio del presupuesto")
    end_date: Optional[date] = Field(None, description="Fecha de finalización del presupuesto")
    status_id: Optional[int] = Field(None, description="ID del estado del presupuesto")
    data: Optional[date] = Field(None, description="Fecha de creación de los datos")

    @model_validator(mode="before")
    def validate_update(cls, values: dict):
        return values
