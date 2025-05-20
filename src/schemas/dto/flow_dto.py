from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class MFlowDTO(BaseModel):
    """
    DTO para transferencia de datos del flujo (m_flows).
    Responsable de la representación y validación de datos.
    """
    id: Optional[int] = Field(None, description="Identificador único del flujo")
    reference: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Referencia del flujo"
    )
    flow_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Nombre descriptivo del flujo"
    )
    active: bool = Field(
        True, description="Indicador si el flujo está activo"
    )
    created_at: Optional[datetime] = Field(
        None, description="Fecha de creación"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Fecha de última actualización"
    )

    class Config:
        from_attributes = True
        anystr_strip_whitespace = True
        schema_extra = {
            "example": {
                "reference": "flow_budget",
                "flow_name": "Presupuesto Flujo",
                "active": True
            }
        }
