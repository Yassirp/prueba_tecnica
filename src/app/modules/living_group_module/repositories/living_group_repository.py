# Archivo generado automáticamente para living_group - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.shared.bases.base_repository import BaseRepository

class LivingGroupRepository(BaseRepository[LivingGroup]):
    def __init__(self, model: type[LivingGroup], db_session: AsyncSession):
        super().__init__(model, db_session)
