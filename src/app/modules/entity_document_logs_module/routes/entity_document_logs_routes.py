# Archivo generado autom�ticamente para entity_document_logs - routes

from fastapi import APIRouter, Depends, Query, status, HTTPException
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
    not_found_message=EntityDocumentLogMessages.ERROR_NOT_FOUND,
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
    entity_document_id: Optional[str] = Query(
        None,
    ),
) -> Dict[str, Any]:        
    try:
        service = EntityDocumentLogsService(db)
        entity_document_logs, total = await service.get_all(limit, offset, order_by, filters, entity_document_id)
        return paginated_response(entity_document_logs, total, limit, offset, )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   


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