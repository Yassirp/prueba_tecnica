from pydantic import BaseModel, Field, model_validator,ConfigDict
from typing import Optional
from decimal import Decimal
from modules.BudgetModule.models.o_budgets_categories import BudgetCategory  
from modules.CategoryModule.models.m_subcategories import MSubCategory


class OBudgetSubcategoryCreate(BaseModel):
    budget_category_id: int
    subcategory_id: int
    total_quantity: float
    total_value: float
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        if not db:
            raise Exception("No se proporcionó la base de datos en el contexto.")

        budget_category_id = values.get('budget_category_id')
        subcategory_id = values.get('subcategory_id')

        if budget_category_id is not None:
            category = db.query(BudgetCategory).filter(BudgetCategory.id == budget_category_id).first()
            if not category:
                raise Exception(f"No se encontró una categoría de presupuesto con id '{budget_category_id}'.")

        if subcategory_id is not None:
            subcategory = db.query(MSubCategory).filter(MSubCategory.id == subcategory_id).first()
            if not subcategory:
                raise Exception(f"No se encontró una sub categoría con el id '{subcategory_id}'.")

        return values

class OBudgetSubcategoryUpdate(BaseModel):
    pass