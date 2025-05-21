from typing import Any, Dict, Optional
from sqlalchemy.sql import Select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import asc, desc

def apply_filters(stmt: Select, model, filters: Dict[str, Any]) -> Select:
    for attr_name, value in filters.items():
        column = getattr(model, attr_name, None)
        if column is not None and value is not None:
            if isinstance(value, str) and "%" in value:
                stmt = stmt.where(column.ilike(value))
            else:
                stmt = stmt.where(column == value)
    return stmt

def apply_order_by(stmt: Select, model, order_by: Optional[str]) -> Select:
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
