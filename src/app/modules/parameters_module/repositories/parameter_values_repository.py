from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.parameters_module.models.m_parameters_values import ParameterValue
from src.app.shared.bases.base_repository import BaseRepository


class ParameterRepository(BaseRepository[ParameterValue]):
    def __init__(self, model: type[ParameterValue], db_session: AsyncSession):
        super().__init__(model, db_session)
