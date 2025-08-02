from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.soccer_field_module.models.soccer_fields import SoccerField
from app.shared.bases.base_repository import BaseRepository

class SoccerFieldRepository(BaseRepository[SoccerField]):
    def __init__(self, model: type[SoccerField], db_session: AsyncSession):
        super().__init__(model, db_session)
