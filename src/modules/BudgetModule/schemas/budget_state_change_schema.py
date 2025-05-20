from pydantic import BaseModel, Field, model_validator
from typing import Optional
from modules.FlowModule.models.m_object_states import MObjectState  
from modules.ParameterModule.models.m_parameters_values import MParameterValue  

class OBudgetStatusChangeCreate(BaseModel):
    budget_id: int = Field(..., description="ID del presupuesto asociado")
    status_id: Optional[int] = Field(None, description="ID del estado asociado")
    type_id: Optional[int] = Field(None, description="ID del tipo de corrección")
    user_id: int = Field(..., description="ID del usuario que realiza el cambio")
    observations: Optional[str] = Field(None, description="Observaciones del cambio")

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
            # Validar existencia de type_id
        type_id = values.get('type_id')
        if type_id is not None:
            type = db.query(MParameterValue).filter(MParameterValue.id == type_id).first()
            if not type:
                raise Exception(f"No se encontró un beneficiario con id '{type_id}'.")

        # Validar existencia de status_id
        status_id = values.get('status_id')
        if status_id is not None:
            status = db.query(MObjectState).filter(MObjectState.id == status_id).first()
            if not status:
                raise Exception(f"No se encontró un estado con id '{status_id}'.")

        # Validar user_id no nulo
        if values.get('user_id') is None:
            raise Exception("El ID del usuario es obligatorio.")

        return values

class OBudgetStatusChangeUpdate(BaseModel):
    observations: Optional[str] = Field(None, description="Nuevas observaciones")

    @model_validator(mode="before")
    def validate_update(cls, values: dict):
        return values
