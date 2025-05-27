from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.shared.bases.base_repository import BaseRepository


class AttributeRepository(BaseRepository[Attribute]):
    def __init__(self, model: type[Attribute], db_session: AsyncSession):
        super().__init__(model, db_session)
