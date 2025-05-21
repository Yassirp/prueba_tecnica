from fastapi import APIRouter, Depends, Query, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from ....config.database.session import get_db
from ..services.entity_type_service import EntityTypeService
from ..schemas.entity_type import EntityTypeCreate, EntityTypeUpdate, EntityTypeOut
from ....shared.utils.request_utils import paginated_response
from ....shared.constants.messages import EntityTypesMessages
from ....decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/entity-types", tags=["Entity Types"])

@router.get("/", response_model=List[EntityTypeOut])
@handle_route_responses(
    success_message=EntityTypesMessages.OK_GET_ALL,
    error_message=EntityTypesMessages.ERROR_GET_ALL
)
async def get_all_entity_types(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=100, description="Número de elementos por página"),
    offset: int = Query(0, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Optional[str] = Query(None, description="Criterios de filtrado en formato JSON (ej: {'name': '%john%', 'state': 0})")
):
    service = EntityTypeService(db)
    entity_types, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    return paginated_response(entity_types, total, limit, offset)


@router.get("/{entity_type_id}", response_model=EntityTypeOut)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_GET,
    error_message=EntityTypesMessages.ERROR_GET,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND
)
async def get_entity_type_by_id(entity_type_id: int, db: AsyncSession = Depends(get_db)):
    service = EntityTypeService(db)
    return await service.get_by_id(entity_type_id)


@router.post("/", response_model=EntityTypeOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_CREATED,
    error_message=EntityTypesMessages.ERROR_CREATED
)
async def create_entity_type(data: EntityTypeCreate, db: AsyncSession = Depends(get_db)):
    service = EntityTypeService(db)
    return await service.create(data.model_dump())


@router.put("/{entity_type_id}", response_model=EntityTypeOut)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_UPDATED,
    error_message=EntityTypesMessages.ERROR_UPDATED,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND
)
async def update_entity_type(entity_type_id: int, data: EntityTypeUpdate, db: AsyncSession = Depends(get_db)):
    service = EntityTypeService(db)
    return await service.update(entity_type_id, data.model_dump(exclude_unset=True))


@router.delete("/{entity_type_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=EntityTypesMessages.OK_DELETED,
    error_message=EntityTypesMessages.ERROR_DELETED,
    not_found_message=EntityTypesMessages.ERROR_NOT_FOUND
)
async def delete_entity_type(entity_type_id: int, db: AsyncSession = Depends(get_db)):
    service = EntityTypeService(db)
    return await service.delete(entity_type_id)
