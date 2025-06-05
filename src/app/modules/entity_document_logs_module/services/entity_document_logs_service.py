# Archivo generado autom�ticamente para entity_document_logs - services
from typing import List, Optional, Dict, Any, Tuple 
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from src.app.shared.constants.messages import EntityDocumentLogMessages
from src.app.modules.entity_document_logs_module.repositories.entity_document_logs_repository import EntityDocumentLogsRepository
from src.app.shared.bases.base_service import BaseService
from src.app.modules.entity_document_logs_module.models.entity_document_logs import EntityDocumentLog
from src.app.modules.entity_document_logs_module.schemas.entity_document_logs_schemas import (
    EntityDocumentLogOut
)

class EntityDocumentLogsService(BaseService[EntityDocumentLog, EntityDocumentLogOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=EntityDocumentLog,
            repository_cls=EntityDocumentLogsRepository,
            db_session=db_session,
            out_schema=EntityDocumentLogOut,
        )
        self.db_session=db_session


    # Obtener todos los logs de documentos
    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        entity_document_id: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.entity_document)
            )   
            conditions = []
            
            # Filtramos por la entidad del documento
            if entity_document_id:
                conditions.append(self.model.entity_document_id == entity_document_id)    
            
            # Filtramos por el tipo de documentop¡
            # Aplicar condiciones al query
            if conditions:
                stmt = stmt.where(and_(*conditions))

            if entity_document_id:
                stmt = stmt.where(self.model.entity_document_id == entity_document_id)

            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)  

            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()  

            total = len(items)
            return items, total
        except Exception as e:
            raise e       

    # Obtener un log de documento por su ID
    async def get_by_id(self, entity_document_log_id: int) -> EntityDocumentLogOut:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.entity_document)
            ).where(self.model.id == entity_document_log_id)

            result = await self.db_session.execute(stmt)
            item = result.scalar_one_or_none()

            if not item:
                raise HTTPException(status_code=404, detail=EntityDocumentLogMessages.ERROR_NOT_FOUND)

            return item 
        except Exception as e:
            raise e
        
    # Crear un nuevo log de documento
    async def create(self, entity_document_log: dict) -> EntityDocumentLogOut:
        try:        
            item = await self.repo.create(entity_document_log)
            return item
        except Exception as e:
            raise e

    # Actualizar un log de documento
    async def update(self, entity_document_log_id: int, entity_document_log: dict) -> EntityDocumentLogOut:
        try:
            item = await self.repo.update(entity_document_log_id, entity_document_log)
            return item
        except Exception as e:
            raise e

        





