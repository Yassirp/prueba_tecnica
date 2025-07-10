from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.user_module.models.user_relationship import UserRelationship
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.app.shared.utils.query_utils import apply_filters, apply_order_by
from sqlalchemy import and_
from src.app.shared.constants.project_enum import Setting

class UserRelationshipRepository(BaseRepository[UserRelationship]):
    def __init__(self, model: type[UserRelationship], db_session: AsyncSession):
        super().__init__(model, db_session)


    async def get_by_user_id(self, user_id: int):
        stmt = select(self.model).where(self.model.user_id == user_id, self.model.deleted_at.is_(None))
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_relationship_id(self, user_relationship_id: int):
        stmt = select(self.model).where(self.model.user_relationship_id == user_relationship_id, self.model.deleted_at.is_(None))
        result = await self.db_session.execute(stmt)
        return result.scalars().all()