# Archivo generado automáticamente para document_rules - services
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.attributes_module.services.attributes_service import AttributeService
from src.app.modules.document_rules_module.models.document_rules import DocumentRule
from src.app.modules.document_rules_module.repositories.document_rules_repository import DocumentRuleRepository
from src.app.modules.document_rules_module.schemas.document_rules_schemas import DocumentRuleOut
from src.app.modules.entity_types_module.services.entity_type_service import EntityTypeService
from src.app.modules.projects_module.services.projects_service import ProjectService
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
        self.project_service = ProjectService(db_session)
        self.entity_type_service = EntityTypeService(db_session)
        self.attribute_service = AttributeService(db_session)
    
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
        
    async def _validate_data(self, data):
        try:
            project_id = data.get("project_id")
            entity_type_id = data.get("entity_type_id")
            document_type_id = data.get("document_type_id")
            project = await self.project_service.get_by_id(project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'",
            )
            
            entity_type = await self.entity_type_service.get_by_id(entity_type_id)
            if not entity_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el tipo de entidad con el id '{entity_type_id}'",
            )

            return True
        except Exception as e:
            raise e
        

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            await self._validate_data(data)
            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e