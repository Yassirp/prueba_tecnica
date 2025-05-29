# Archivo generado automáticamente para document_rules - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.document_rules_module.models.document_rules import DocumentRule
from src.app.modules.document_rules_module.repositories.document_rules_repository import DocumentRuleRepository
from src.app.modules.document_rules_module.schemas.document_rules_schemas import DocumentRuleOut
from src.app.shared.bases.base_service import BaseService
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class DocumentRuleService(BaseService[DocumentRule, DocumentRuleOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=DocumentRule,
            repository_cls=DocumentRuleRepository,
            db_session=db_session,
            out_schema=DocumentRuleOut,
        )
        self.db_session=db_session

    
    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.project),
                selectinload(self.model.document_type),
                selectinload(self.model.stage),
                selectinload(self.model.entity_type),
                )

            # Aquí puedes aplicar filtros, orden y paginación si los necesitas.
            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)
            
            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()

            # Opcional: Si tienes filtros aplicados en SQL puedes contar antes,
            # si no, simplemente haces len().
            total = len(items)
            return items, total
        except Exception as e:
            raise e