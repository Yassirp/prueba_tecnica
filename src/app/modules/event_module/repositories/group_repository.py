# Archivo generado automáticamente para event - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.event_module.models.groups import Group
from src.app.shared.bases.base_repository import BaseRepository

class GroupRepository(BaseRepository[Group]):
    def __init__(self, model: type[Group], db_session: AsyncSession):
        super().__init__(model, db_session)
