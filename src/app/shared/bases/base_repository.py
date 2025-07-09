from sqlalchemy import and_
from typing import (
    TypeVar,
    Generic,
    Type,
    Optional,
    Tuple,
    Any,
    Dict,
    Sequence,
    Protocol,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.app.shared.constants.project_enum import Setting
from src.app.shared.utils.query_utils import apply_filters, apply_order_by
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime

T = TypeVar("T", bound=BaseModel)

class HasId(Protocol):
    id: Any

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get_by_id(self, id: Any) -> Optional[T]:
        try:
            query = select(self.model).where(self.model.id == id, self.model.deleted_at.is_(None))
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
    ) -> Tuple[Sequence[T], int]:
        try:
            stmt = select(self.model).where(self.model.state == Setting.STATUS.value)
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

    async def create(self, data: Dict[str, Any]) -> T:
        try:
            instance = self.model(**data)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)
            return instance
        except Exception as e:
            raise e

    async def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        try:
            query = update(self.model).where(self.model.id == id).values(**data)
            await self.db_session.execute(query)
            await self.db_session.commit()
            return await self.get_by_id(id)
        except Exception as e:
            raise e

    async def delete(self, id: Any) -> bool:
        try:
            query = (
            update(self.model)
            .where(self.model.id == id)
            .values(
                deleted_at=datetime.utcnow(),
                is_active=False
            )
            )
            result = await self.db_session.execute(query)
            await self.db_session.commit()
            return result.rowcount > 0
        except Exception as e:
            raise e
