from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.living_group_module.models.events import Event
from src.app.modules.living_group_module.repositories.event_repository import EventRepository
from src.app.modules.living_group_module.schemas.event_schemas import EventOut

class EventService(BaseService[Event, EventOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Event,
            repository_cls=EventRepository,
            db_session=db_session,
            out_schema=EventOut,
        ) 