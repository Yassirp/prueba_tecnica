from typing import Any, Dict, Optional, TypeVar, Union
from sqlalchemy.sql import Select
from sqlalchemy import and_
import json
from fastapi import HTTPException

T = TypeVar("T")

def apply_filters(
    query: Select, model: Any, filters: Union[Dict[str, Any], str]
) -> Select:
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
                status_code=400, detail="Invalid JSON in filters parameter"
            )

    if not isinstance(filters, dict):
        return query

    conditions = []
    for key, value in filters.items():
        if hasattr(model, key):
            column = getattr(model, key)
            if isinstance(value, str) and "%" in value:
                conditions.append(column.ilike(value))
            else:
                conditions.append(column == value)

    if conditions:
        query = query.where(and_(*conditions))
    return query


def apply_order_by(query: Select, model: Any, order_by: Optional[str]) -> Select:
    """
    Ejemplo de uso:

    order_by = "id:asc"
    order_by = "name:desc"
    order_by = "created_at:asc"
    """
    if not order_by:
        return query

    try:
        field, direction = order_by.split(":")
        if hasattr(model, field):
            column = getattr(model, field)
            if direction.lower() == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    except ValueError:
        pass

    return query
