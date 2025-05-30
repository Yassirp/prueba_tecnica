# Archivo generado autom�ticamente para entity_document_logs - routes

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.entity_document_logs_module.schemas.entity_document_logs_schemas import (
    EntityDocumentLogCreate,
    EntityDocumentLogUpdate,
    EntityDocumentLogOut
)
from src.app.modules.entity_document_logs_module.services.entity_document_logs_service import EntityDocumentLogsService
from src.app.shared.constants.messages import EntityDocumentLogMessages
from src.app.shared.utils.request_utils import paginated_response
from src.app.decorators.route_responses import handle_route_responses
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/entity-document-logs", tags=["Entity Document Logs"])   


@router.get("/get-all", response_model=List[EntityDocumentLogOut])
@handle_route_responses(
    success_message=EntityDocumentLogMessages.OK_GET_ALL,
    error_message=EntityDocumentLogMessages.ERROR_GET_ALL,
)

# Obtener todos los logs de documentos
async def get_all_entity_document_logs(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Número de elementos por página"
    ),
    offset: Optional[int] = Query(
        None, ge=0, description="Número de elementos a omitir"
    ),
    order_by: Optional[str] = Query(
        None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"
    ),
    filters: Optional[str] = Query(
        None,
        description="Criterios de filtrado en formato JSON (ej: {'name': '%john%', 'state': 0})",
    ),
) -> Dict[str, Any]:
    service = EntityDocumentLogsService(db)
    return await service.get_all(limit, offset, order_by, filters)  


# Obtener un log de documento por su ID
@router.get("/get-by-id/{entity_document_log_id}", response_model=EntityDocumentLogOut)
@handle_route_responses(
    success_message=EntityDocumentLogMessages.OK_GET,
    error_message=EntityDocumentLogMessages.ERROR_GET,
    not_found_message=EntityDocumentLogMessages.ERROR_NOT_FOUND,
)

# Obtener un log de documento por su ID
async def get_entity_document_log_by_id(
    entity_document_log_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = EntityDocumentLogsService(db)
    return await service.get_by_id(entity_document_log_id)


# Crear un nuevo log de documento
@router.post("/create", response_model=EntityDocumentLogOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=EntityDocumentLogMessages.OK_CREATED,
    error_message=EntityDocumentLogMessages.ERROR_CREATED,
)

# Crear un nuevo log de documento
async def create_entity_document_log(
    entity_document_log: EntityDocumentLogCreate,
    db: AsyncSession = Depends(get_db)
):
    service = EntityDocumentLogsService(db)
    return await service.create(entity_document_log)


# Actualizar un log de documento
@router.put("/update/{entity_document_log_id}", response_model=EntityDocumentLogOut)
@handle_route_responses(
    success_message=EntityDocumentLogMessages.OK_UPDATED,
    error_message=EntityDocumentLogMessages.ERROR_UPDATED,
    not_found_message=EntityDocumentLogMessages.ERROR_NOT_FOUND,
)

# Actualizar un log de documento
async def update_entity_document_log(
    entity_document_log_id: int,
    entity_document_log: EntityDocumentLogUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = EntityDocumentLogsService(db)
    return await service.update(entity_document_log_id, entity_document_log)    


# Eliminar un log de documento
@router.delete("/delete/{entity_document_log_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=EntityDocumentLogMessages.OK_DELETED,
    error_message=EntityDocumentLogMessages.ERROR_DELETED,  
    not_found_message=EntityDocumentLogMessages.ERROR_NOT_FOUND,
)

# Eliminar un log de documento  
async def delete_entity_document_log(
    entity_document_log_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = EntityDocumentLogsService(db)
    return await service.delete(entity_document_log_id)

