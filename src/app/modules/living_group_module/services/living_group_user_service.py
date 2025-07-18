from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser
from src.app.modules.living_group_module.repositories.living_group_users_repository import LivingGroupUserRepository
from src.app.modules.living_group_module.schemas.living_group_user_schemas import LivingGroupUserOut

class LivingGroupUserService(BaseService[LivingGroupUser, LivingGroupUserOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=LivingGroupUser,
            repository_cls=LivingGroupUserRepository,
            db_session=db_session,
            out_schema=LivingGroupUserOut,
        )
