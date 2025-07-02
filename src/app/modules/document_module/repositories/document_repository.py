from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.document_module.models.documents import Document
from src.app.shared.bases.base_repository import BaseRepository

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, model: type[Document], db_session: AsyncSession):
        super().__init__(model, db_session)
