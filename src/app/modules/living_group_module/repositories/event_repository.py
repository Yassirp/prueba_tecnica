from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.living_group_module.models.events import Event
from src.app.shared.bases.base_repository import BaseRepository

class EventRepository(BaseRepository[Event]):
    def __init__(self, model: type[Event], db_session: AsyncSession):
        super().__init__(model, db_session) 