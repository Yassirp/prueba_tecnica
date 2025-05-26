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
from src.app.shared.utils.query_utils import apply_filters, apply_order_by
from src.app.shared.bases.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)

class HasId(Protocol):
    id: Any

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get_by_id(self, id: Any) -> Optional[T]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Sequence[T], int]:
        stmt = select(self.model)

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

    async def create(self, data: Dict[str, Any]) -> T:
        instance = self.model(**data)
        self.db_session.add(instance)
        await self.db_session.commit()
        await self.db_session.refresh(instance)
        return instance

    async def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        query = update(self.model).where(self.model.id == id).values(**data)
        await self.db_session.execute(query)
        await self.db_session.commit()
        return await self.get_by_id(id)

    async def delete(self, id: Any) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.rowcount > 0