from sqlalchemy.ext.asyncio import AsyncSession
from ..models.entity_types import EntityType
from ....shared.bases.base_repository import BaseRepository


class EntityTypeRepository(BaseRepository[EntityType]):
    def __init__(self, db: AsyncSession):
        super().__init__(EntityType, db)
