from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class LivingGroupUserRepository(BaseRepository[LivingGroupUser]):
    def __init__(self, model: type[LivingGroupUser], db_session: AsyncSession):
        super().__init__(model, db_session)
