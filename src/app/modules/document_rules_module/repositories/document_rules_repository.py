from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.document_rules_module.models.document_rules import DocumentRule
from src.app.shared.bases.base_repository import BaseRepository


class DocumentRuleRepository(BaseRepository[DocumentRule]):
    def __init__(self, model: type[DocumentRule], db_session: AsyncSession):
        super().__init__(model, db_session)
