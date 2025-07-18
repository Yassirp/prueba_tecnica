from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.ubication_module.models.municipalities import Municipality
from src.app.shared.bases.base_repository import BaseRepository

class MunicipalityRepository(BaseRepository[Municipality]):
    def __init__(self, db_session: AsyncSession, model: type[Municipality] = Municipality):
        super().__init__(model, db_session)