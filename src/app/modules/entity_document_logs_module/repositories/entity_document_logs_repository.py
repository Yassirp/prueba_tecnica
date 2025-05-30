# Archivo generado autom�ticamente para entity_document_logs - repositories

from src.app.modules.entity_document_logs_module.models.entity_document_logs import EntityDocumentLog
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class EntityDocumentLogsRepository(BaseRepository[EntityDocumentLog]):
    def __init__(self, model: type[EntityDocumentLog], db_session: AsyncSession):
        super().__init__(model, db_session)

