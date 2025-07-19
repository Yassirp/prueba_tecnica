# Archivo generado automáticamente para living_group - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy import select, and_
from src.app.shared.utils.query_utils import apply_filters, apply_order_by
from sqlalchemy.orm import selectinload
from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser
class LivingGroupRepository(BaseRepository[LivingGroup]):
    def __init__(self, model: type[LivingGroup], db_session: AsyncSession):
        super().__init__(model, db_session)

    async def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = {}) -> tuple:
        try:
            stmt = select(self.model)
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

            stmt = self._load_relations(stmt)
            result = await self.db_session.execute(stmt)
            return result.scalars().all(), total
        except Exception as e:
            raise e

    async def get_by_id_with_relations(self, living_group_id: int) -> LivingGroup | None:        
            stmt = select(self.model)
            stmt = stmt.where(self.model.id == living_group_id)
            stmt = self._load_relations(stmt)
            result = await self.db_session.execute(stmt)
            return result.scalars().first()
    
    def _load_relations(self, query):
        return query.options(
                selectinload(self.model.getSede),
                selectinload(self.model.getLivingGroupUsers)
                .selectinload(LivingGroupUser.getUser)
            )
    