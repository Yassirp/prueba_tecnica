from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from src.app.modules.ubication_module.models.countries import Country
from src.app.modules.ubication_module.models.departments import Department
from src.app.shared.bases.base_repository import BaseRepository
from src.app.shared.utils.query_utils import apply_filters, apply_order_by

class CountryRepository(BaseRepository[Country]):
    def __init__(self, model: type[Country], db_session: AsyncSession):
        super().__init__(model, db_session)
        
    async def get_all_with_relationships(self, limit: int, offset: int, order_by: str, filters: dict = {}) -> tuple:
        try:
            stmt = select(Country)
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

            stmt = stmt.options(
                selectinload(Country.departments).selectinload(Department.municipalities)
            )
            result = await self.db_session.execute(stmt)
            return result.scalars().all(), total
        except Exception as e:
            raise e