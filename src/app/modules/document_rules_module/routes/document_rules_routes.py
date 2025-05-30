# Archivo generado automáticamente para document_rules - routes
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.document_rules_module.schemas.document_rules_schemas import (
    DocumentRuleCreate,
    DocumentRuleOut,
    DocumentRuleUpdate
)
from src.app.modules.document_rules_module.services.document_rules_service import DocumentRuleService
from src.app.shared.constants.messages import DocumentRuleMessages
from src.app.shared.utils.request_utils import paginated_response
from src.app.decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/document-rules", tags=["Document Rules"])


@router.get("/get-all", response_model=List[DocumentRuleOut])
@handle_route_responses(
    success_message=DocumentRuleMessages.OK_GET_ALL,
    error_message=DocumentRuleMessages.ERROR_GET_ALL,
)
async def get_all_document_rule(
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
    entity_type_id: Optional[int] = Query(None),
    document_type_id: Optional[int] = Query(None),
    stage_id: Optional[int] = Query(None),
    id: Optional[int] = Query(None),
) -> Dict[str, Any]:
    try:
        service = DocumentRuleService(db)
        attributes, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters, entity_type_id=entity_type_id, 
        document_type_id=document_type_id, stage_id=stage_id, id=id
        )
        return paginated_response(attributes, total, limit, offset)
    except Exception as e:
        raise e


@router.get("/get-by-id/{document_rule_id}", response_model=DocumentRuleOut)
@handle_route_responses(
    success_message=DocumentRuleMessages.OK_GET,
    error_message=DocumentRuleMessages.ERROR_GET,
    not_found_message=DocumentRuleMessages.ERROR_NOT_FOUND,
)
async def get_document_rule_by_id(
    document_rule_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = DocumentRuleService(db)
        return await service.get_by_id(document_rule_id)
    except Exception as e:
        raise e


@router.post("/create", response_model=DocumentRuleOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=DocumentRuleMessages.OK_CREATED,
    error_message=DocumentRuleMessages.ERROR_CREATED,
)
async def create_document_rule(
    data: DocumentRuleCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:    
        service = DocumentRuleService(db)
        return await service.create(data.model_dump())
    except Exception as e:
        raise e


@router.put("/update/{document_rule_id}", response_model=DocumentRuleOut)
@handle_route_responses(
    success_message=DocumentRuleMessages.OK_UPDATED,
    error_message=DocumentRuleMessages.ERROR_UPDATED,
    not_found_message=DocumentRuleMessages.ERROR_NOT_FOUND,
)
async def update_entity_type(
    document_rule_id: int, data: DocumentRuleUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = DocumentRuleService(db)
        return await service.update(document_rule_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise e


@router.delete("/delete/{document_rule_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=DocumentRuleMessages.OK_DELETED,
    error_message=DocumentRuleMessages.ERROR_DELETED,
    not_found_message=DocumentRuleMessages.ERROR_NOT_FOUND,
)
async def delete_entity_type(
    document_rule_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    try:
        service = DocumentRuleService(db)
        return await service.delete(document_rule_id)
    except Exception as e: 
        raise e
