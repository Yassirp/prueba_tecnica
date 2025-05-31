# Archivo generado automáticamente para entity_documents - routes
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.entity_documents_module.schemas.entity_documents_schemas import (
    EntityDocumentCreate, 
    EntityDocumentOut,
    EntityDocumentUpdate
    )
from src.app.modules.entity_documents_module.services.entity_documents_service import EntityDocumentService
from src.app.shared.utils.request_utils import paginated_response
from src.app.shared.constants.messages import EntityDocumentMessages
from src.app.decorators.route_responses import handle_route_responses


router = APIRouter(prefix="/entity-documents", tags=["Entity Documents"])


@router.get("/get-all", response_model=List[EntityDocumentOut])
@handle_route_responses(
    success_message=EntityDocumentMessages.OK_GET_ALL,
    error_message=EntityDocumentMessages.ERROR_GET_ALL,
)
async def get_all_entity_docuemnt(
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
    project_id: Optional[int] =  Query(None),
    document_status_id: Optional[int] =  Query(None),
    entity_type_id: Optional[int] =  Query(None),
    stage_id: Optional[int] =  Query(None),
) -> Dict[str, Any]:
    try:
        service = EntityDocumentService(db)
        entity_docuemnt, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters , project_id=project_id, 
        document_status_id=document_status_id, entity_type_id=entity_type_id, stage_id=stage_id
        )
        return paginated_response(entity_docuemnt, total, limit, offset)
    except Exception as e:
        raise e


@router.get("/get-by-id/{entity_docuemnt_id}", response_model=EntityDocumentOut)
@handle_route_responses(
    success_message=EntityDocumentMessages.OK_GET,
    error_message=EntityDocumentMessages.ERROR_GET,
    not_found_message=EntityDocumentMessages.ERROR_NOT_FOUND,
)
async def get_entity_docuemnt_by_id(
    entity_docuemnt_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = EntityDocumentService(db)
        return await service.get_by_id(entity_docuemnt_id)
    except Exception as e:
        raise e


@router.post("/create", response_model=EntityDocumentOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=EntityDocumentMessages.OK_CREATED,
    error_message=EntityDocumentMessages.ERROR_CREATED,
)
async def create_entity_docuemnt(
    data: EntityDocumentCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:    
        service = EntityDocumentService(db)
        return await service.create(data.model_dump())
    except Exception as e:
        raise e
    

@router.put("/update/{entity_docuemnt_id}", response_model=EntityDocumentOut)
@handle_route_responses(
    success_message=EntityDocumentMessages.OK_UPDATED,
    error_message=EntityDocumentMessages.ERROR_UPDATED,
    not_found_message=EntityDocumentMessages.ERROR_NOT_FOUND,
)
async def update_entity_docuemnt(
    entity_docuemnt_id: int, data: EntityDocumentUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = EntityDocumentService(db)
        return await service.update(entity_docuemnt_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise e
    

@router.delete("/delete/{entity_docuemnt_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=EntityDocumentMessages.OK_DELETED,
    error_message=EntityDocumentMessages.ERROR_DELETED,
    not_found_message=EntityDocumentMessages.ERROR_NOT_FOUND,
)
async def delete_entity_docuemnt(
    entity_docuemnt_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    try:
        service = EntityDocumentService(db)
        return await service.delete(entity_docuemnt_id)
    except Exception as e: 
        raise e