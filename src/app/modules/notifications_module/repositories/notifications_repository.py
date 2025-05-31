# Archivo generado autom�ticamente para notifications - repositories
from src.app.modules.notifications_module.models.notifications import Notification
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class NotificationsRepository(BaseRepository[Notification]):
    def __init__(self, model: type[Notification], db_session: AsyncSession):
        super().__init__(model, db_session)