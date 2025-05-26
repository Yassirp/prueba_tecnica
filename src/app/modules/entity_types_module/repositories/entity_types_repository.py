from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_repository import BaseRepository
from src.app.modules.entity_types_module.models.entity_types import EntityType


class EntityTypeRepository(BaseRepository[EntityType]):
    def __init__(self, model: type[EntityType], db_session: AsyncSession):
        super().__init__(model, db_session)
