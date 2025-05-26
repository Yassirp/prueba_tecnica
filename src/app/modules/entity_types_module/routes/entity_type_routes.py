from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.entity_types_module.services.entity_type_service import (
    EntityTypeService,
)
from src.app.modules.entity_types_module.schemas.entity_types_schemas import (
    EntityTypeCreate,
    EntityTypeUpdate,
    EntityTypeOut,
)
from src.app.shared.utils.request_utils import paginated_response
from src.app.shared.constants.messages import EntityTypesMessages
from src.app.decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/entity-types", tags=["Entity Types"])


@router.get("/get-all", response_model=List[EntityTypeOut])
@handle_route_responses(
    success_message=EntityTypesMessages.OK_GET_ALL,
    error_message=EntityTypesMessages.ERROR_GET_ALL,
)
async def get_all_entity_types(
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
    service = EntityTypeService(db)
    entity_types, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters
    )
    return paginated_response(entity_types, total, limit, offset)


@router.get("/get-by-id/{entity_type_id}", response_model=EntityTypeOut)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_GET,
    error_message=EntityTypesMessages.ERROR_GET,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND,
)
async def get_entity_type_by_id(
    entity_type_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    service = EntityTypeService(db)
    return await service.get_by_id(entity_type_id)


@router.post("/create", response_model=EntityTypeOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_CREATED,
    error_message=EntityTypesMessages.ERROR_CREATED,
)
async def create_entity_type(
    data: EntityTypeCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    service = EntityTypeService(db)
    return await service.create(data.model_dump())


@router.put("/update/{entity_type_id}", response_model=EntityTypeOut)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_UPDATED,
    error_message=EntityTypesMessages.ERROR_UPDATED,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND,
)
async def update_entity_type(
    entity_type_id: int, data: EntityTypeUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    service = EntityTypeService(db)
    return await service.update(entity_type_id, data.model_dump(exclude_unset=True))


@router.delete("/delete/{entity_type_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_DELETED,
    error_message=EntityTypesMessages.ERROR_DELETED,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND,
)
async def delete_entity_type(
    entity_type_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    service = EntityTypeService(db)
    return await service.delete(entity_type_id)
