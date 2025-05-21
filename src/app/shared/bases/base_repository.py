from typing import TypeVar, Generic, Type, Optional, List, Tuple, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..utils.query_utils import apply_filters, apply_order_by

T = TypeVar("T")  # Modelo SQLAlchemy

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: Any) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[dict] = None
    ) -> Tuple[List[T], int]:
        stmt = select(self.model)

        if filters:
            stmt = apply_filters(stmt, self.model, filters)

        if order_by:
            stmt = apply_order_by(stmt, self.model, order_by)

        count_stmt = stmt.with_only_columns(self.model.id).order_by(None)
        count_result = await self.session.execute(count_stmt)
        total = len(count_result.scalars().all())

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all(), total

    async def create(self, data: dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: Any, data: dict) -> Optional[T]:
        instance = await self.get_by_id(id)
        if not instance:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: Any) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False

        await self.session.delete(instance)
        await self.session.commit()
        return True
