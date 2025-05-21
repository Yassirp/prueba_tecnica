from sqlalchemy.ext.asyncio import AsyncSession
from ....shared.bases.base_service import BaseService
from ..models.entity_types import EntityType
from ..repositories.entity_types_repository import EntityTypeRepository
from ..schemas.entity_type import EntityTypeOut

class EntityTypeService(BaseService[EntityType, EntityTypeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=EntityType,
            repository_cls=EntityTypeRepository,
            db_session=db_session,
            out_schema=EntityTypeOut
        )