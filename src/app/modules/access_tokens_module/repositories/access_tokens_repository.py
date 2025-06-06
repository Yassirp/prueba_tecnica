# Archivo generado automáticamente para access_tokens - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.access_tokens_module.models.access_tokens import AccessToken
from src.app.shared.bases.base_repository import BaseRepository

class AccessTokenRepository(BaseRepository[AccessToken]):
    def __init__(self, model: type[AccessToken], db_session: AsyncSession):
        super().__init__(model, db_session)
