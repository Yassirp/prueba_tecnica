from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.stages_module.models.stages import Stage
from src.app.shared.bases.base_repository import BaseRepository

class StageRepository(BaseRepository[Stage]):
    def __init__(self, model: type[Stage], db_session: AsyncSession):
        super().__init__(model, db_session)
