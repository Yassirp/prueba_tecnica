from pydantic import BaseModel, Field, model_validator
from typing import Optional
from decimal import Decimal
from modules.BudgetModule.models.o_budgets_subcategories import BudgetSubcategory 
from modules.CategoryModule.models.m_products import MProduct 
class OBudgetSubcategoryDetailCreate(BaseModel):
    budget_subcategory_id: int = Field(..., description="ID de la subcategoría de presupuesto asociada")
    product_id: int = Field(..., description="ID del producto")
    # incidence: Optional[Decimal] = Field(None, description="Incidencia del producto")
    total_value: Decimal = Field(..., description="Valor total del producto")
    # unit_value: Decimal = Field(..., description="Valor unitario del producto")
    quantity: Decimal = Field(..., description="Cantidad de productos")

    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        budget_subcategory_id = values.get('budget_subcategory_id')
        product_id = values.get('product_id')
        if budget_subcategory_id is not None:
            subcategory = db.query(BudgetSubcategory).filter(BudgetSubcategory.id == budget_subcategory_id).first()
            if not subcategory:
                raise Exception(f"No se encontró una subcategoría con id '{budget_subcategory_id}'.")
            
        if product_id is not None:
            product = db.query(MProduct).filter(MProduct.id == product_id).first()
            if not product:
                raise Exception(f"No se encontró un producto con id '{product_id}'.")
            
        return values

class OBudgetSubcategoryDetailUpdate(BaseModel):
    incidence: Optional[Decimal] = Field(None, description="Incidencia del producto")
    total_value: Optional[Decimal] = Field(None, description="Valor total del producto")
    unit_value: Optional[Decimal] = Field(None, description="Valor unitario del producto")
    quantity: Optional[Decimal] = Field(None, description="Cantidad de productos")

    @model_validator(mode="before")
    def validate_update(cls, values: dict):
        return values
