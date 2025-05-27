from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.shared.bases.base_repository import BaseRepository


class ParameterRepository(BaseRepository[Parameter]):
    def __init__(self, model: type[Parameter], db_session: AsyncSession):
        super().__init__(model, db_session)
