# Archivo generado automáticamente para sedes - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.sedes_module.models.sedes import Sede
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy import select, and_
from src.app.shared.utils.query_utils import apply_filters, apply_order_by
from sqlalchemy.orm import selectinload
from src.app.modules.sedes_module.models.sedes_members import SedesMember

class SedeRepository(BaseRepository[Sede]):
    def __init__(self, model: type[Sede], db_session: AsyncSession):
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

    async def get_by_id_with_relations(self, sede_id: int) -> Sede | None:        
            stmt = select(self.model)
            stmt = stmt.where(self.model.id == sede_id)
            stmt = self._load_relations(stmt)
            result = await self.db_session.execute(stmt)
            return result.scalars().first()
    
    def _load_relations(self, query):
        return query.options(
                selectinload(self.model.getDepartment),
                selectinload(self.model.getMunicipality),
                selectinload(self.model.getLivingGroups),
                selectinload(self.model.getSedesMembers).selectinload(SedesMember.getUser),
                selectinload(self.model.getSedesMembers).selectinload(SedesMember.getType)
            )
    