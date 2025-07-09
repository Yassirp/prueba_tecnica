from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_
from typing import Optional, Tuple, Sequence, Dict, Any
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from src.app.shared.bases.base_repository import BaseRepository
from src.app.shared.constants.project_enum import Setting
from src.app.shared.utils.query_utils import apply_filters, apply_order_by


class ParameterRepository(BaseRepository[Parameter]):
    def __init__(self, model: type[Parameter], db_session: AsyncSession):
        super().__init__(model, db_session)

    async def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = "id:asc", filters: dict = {}) -> tuple:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.values)
                    .selectinload(ParameterValue.children)
            )
            conditions = [self.model.deleted_at.is_(None)]
            stmt = stmt.where(and_(*conditions))
            if filters:
                stmt = self._filter_by_parameters(stmt, filters)
            if order_by:
                stmt = apply_order_by(stmt, self.model, order_by)
            count_stmt = stmt.with_only_columns(self.model.id).order_by(None)
            count_result = await self.db_session.execute(count_stmt)
            total = len(count_result.scalars().all())
            if offset is not None:
                stmt = stmt.offset(offset)
            if limit is not None:
                stmt = stmt.limit(limit)
            result = await self.db_session.execute(stmt)
            return result.scalars().all(), total
        except Exception as e:
            raise e
        
    def _filter_by_parameters(self, stmt, filters: dict):
        if filters:
            if 'keys' in filters:
                keys = filters['keys']
                if isinstance(keys, str):
                    keys = [k.strip() for k in keys.split(",") if k.strip()]
                stmt = stmt.where(self.model.key.in_(keys))
            
            stmt = apply_filters(stmt, self.model, filters)
        return stmt