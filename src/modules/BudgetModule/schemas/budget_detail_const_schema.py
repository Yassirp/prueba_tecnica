from pydantic import BaseModel, Field, model_validator
from typing import Optional
from decimal import Decimal
from modules.BudgetModule.models.o_budgets import OBudget  # Ajusta el import si es necesario
from modules.ParameterModule.models.m_parameters_values import MParameterValue  # Ajusta la ruta

class OBudgetDetailCostCreate(BaseModel):
    concept_id: int = Field(..., description="ID del concepto")
    budget_id: int = Field(..., description="ID del presupuesto asociado")
    type_id: int = Field(..., description="ID del tipo de costo")
    value: Decimal = Field(..., description="Valor del costo")
    percentage: Decimal = Field(..., description="Porcentaje del costo")

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
            # Validar que concept_id exista
        concept_id = values.get('concept_id')
        if concept_id:
            exists_concept = db.query(MParameterValue).filter(MParameterValue.id == concept_id).first()
            if not exists_concept:
                raise Exception(f"El concepto con id '{concept_id}' no existe.")

        # Validar que type_id exista
        type_id = values.get('type_id')
        if type_id:
            exists_type = db.query(MParameterValue).filter(MParameterValue.id == type_id).first()
            if not exists_type:
                raise Exception(f"El tipo de costo con id '{type_id}' no existe.")

        # Validar que budget_id exista
        budget_id = values.get('budget_id')
        if budget_id:
            exists_budget = db.query(OBudget).filter(OBudget.id == budget_id).first()
            if not exists_budget:
                raise Exception(f"El presupuesto con id '{budget_id}' no existe.")

        return values

class OBudgetDetailCostUpdate(BaseModel):
    value: Optional[Decimal] = Field(None, description="Valor actualizado del costo")
    percentage: Optional[Decimal] = Field(None, description="Porcentaje actualizado del costo")

    @model_validator(mode="before")
    def validate_update(cls, values: dict):
        # Opcionalmente podrías validar que value o percentage no sean negativos, por ejemplo
        value = values.get('value')
        if value is not None and value < 0:
            raise Exception("El valor del costo no puede ser negativo.")
        
        percentage = values.get('percentage')
        if percentage is not None and (percentage < 0 or percentage > 100):
            raise Exception("El porcentaje debe estar entre 0 y 100.")
        
        return values
