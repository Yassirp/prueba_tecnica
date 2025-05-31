# Archivo generado automáticamente para entity_documents - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_repository import BaseRepository
from src.app.modules.entity_documents_module.models.entity_documents import EntityDocument


class EntityDocumentRepository(BaseRepository[EntityDocument]):
    def __init__(self, model: type[EntityDocument], db_session: AsyncSession):
        super().__init__(model, db_session)
