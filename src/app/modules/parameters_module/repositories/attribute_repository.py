from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.parameters_module.models.parameters import Attribute
from src.app.shared.bases.base_repository import BaseRepository


class AttributeRepository(BaseRepository[Attribute]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(model=Attribute, db_session=db_session)
