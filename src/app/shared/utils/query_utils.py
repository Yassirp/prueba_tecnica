from typing import Any, Dict, Optional
from sqlalchemy.sql import Select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import asc, desc
import json
from fastapi import HTTPException, status

def apply_filters(stmt: Select, model, filters: Dict[str, Any]) -> Select:
    """
    Ejemplo de uso:
    
    # Filtro exacto
    filters = {
        "name": "John",
        "age": 25
    }
    
    # Filtro con LIKE
    filters = {
        "name": "%john%",  # Busca nombres que contengan "john"
        "email": "john%"   # Busca emails que empiecen con "john"
    }
    
    # Combinación de filtros
    filters = {
        "name": "%john%",
        "age": 25,
        "city": "New York"
    }
    """
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El formato de los filtros no es válido. Debe ser un JSON válido."
            )
    
    for attr_name, value in filters.items():
        column = getattr(model, attr_name, None)
        if column is not None and value is not None:
            if isinstance(value, str) and "%" in value:
                stmt = stmt.where(column.ilike(value))
            else:
                stmt = stmt.where(column == value)
    return stmt

def apply_order_by(stmt: Select, model, order_by: Optional[str]) -> Select:
    """
    Ejemplo de uso:
    
    order_by = "id:asc"
    order_by = "name:desc"
    order_by = "created_at:asc"
    """
    if not order_by:
        return stmt

    try:
        field, direction = order_by.split(":")
        column: InstrumentedAttribute = getattr(model, field, None)
        if column is not None:
            stmt = stmt.order_by(desc(column) if direction.lower() == "desc" else asc(column))
    except ValueError:
        pass  # orden malformado, ignoramos

    return stmt
