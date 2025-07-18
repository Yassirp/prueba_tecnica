from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.schemas.living_group_schemas import LivingGroupOut
from typing import Optional, Dict


class LivingGroupService(BaseService[LivingGroup, LivingGroupOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=LivingGroup,
            repository_cls=LivingGroupRepository,
            db_session=db_session,
            out_schema=LivingGroupOut,
        )

    async def get_all_with_relations(self, limit: Optional[int] = None, offset: Optional[int] = None, order_by: Optional[str] = None, filters: Optional[Dict[str, str]] = None):
        return await self.repo.get_all_with_relationships(limit=limit, offset=offset, order_by=order_by, filters=filters)

    async def get_by_id_with_relations(self, living_group_id: int):
        return await self.repo.get_by_id_with_relations(living_group_id)