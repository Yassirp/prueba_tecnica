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

    async def get_by_id(self, id: Any) -> Optional[Parameter]:
        try:
            query = select(self.model).options(
                selectinload(self.model.values)
                    .selectinload(ParameterValue.children)
                    .selectinload(ParameterValue.children)
                    .selectinload(ParameterValue.children)
            ).where(self.model.id == id, self.model.deleted_at.is_(None))
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Sequence[Parameter], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.values)
                    .selectinload(ParameterValue.children)
                    .selectinload(ParameterValue.children)
                    .selectinload(ParameterValue.children)
            ).where(self.model.state == Setting.STATUS.value)
            conditions = [self.model.deleted_at.is_(None)]

            stmt = stmt.where(and_(*conditions))
            if filters:
                stmt = apply_filters(stmt, self.model, filters)

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
