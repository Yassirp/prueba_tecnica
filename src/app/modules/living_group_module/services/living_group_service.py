from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.schemas.living_group_schemas import LivingGroupOut

class LivingGroupService(BaseService[LivingGroup, LivingGroupOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=LivingGroup,
            repository_cls=LivingGroupRepository,
            db_session=db_session,
            out_schema=LivingGroupOut,
        )
