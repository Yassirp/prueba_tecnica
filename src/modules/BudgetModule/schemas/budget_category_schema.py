from pydantic import BaseModel, Field, model_validator
from typing import Optional
from modules.BudgetModule.models.o_budgets import OBudget  # Ajusta la ruta si es necesario
from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
class OBudgetCategoryCreate(BaseModel):
    budget_id: int = Field(..., description="ID del presupuesto asociado")
    category_id: int = Field(..., description="ID de la categoría")

    @model_validator(mode='before')
    def validate_foreign_keys_and_name(cls, values: dict, info):
        db = info.context.get("db", None)
        budget_id = values.get('budget_id')
        if budget_id:
            exists_budget = db.query(OBudget).filter(OBudget.id == budget_id).first()
            if not exists_budget:
                raise Exception(f"El presupuesto con id '{budget_id}' no existe.")
            
            
        category_id = values.get('category_id')
        if category_id:
            exists_budget = db.query(MCategoryRegion).filter(MCategoryRegion.id == category_id).first()
            if not exists_budget:
                raise Exception(f"La categoría con id '{category_id}' no existe.")

        return values

class OBudgetCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Nombre de la categoría")

    @model_validator(mode='before')
    def validate_update_name(cls, values: dict):
        name = values.get('name')
        if name is not None and not name.strip():
            raise Exception("El nombre de la categoría no puede estar vacío o ser solo espacios.")
        return values
