from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db


from src.app.modules.stages_module.schemas.stages_schemas import (
    StageCreate, StageOut, StageUpdate
)
from src.app.modules.stages_module.services.stages_services import StageService
from src.app.shared.utils.request_utils import paginated_response
from src.app.shared.constants.messages import StagesMessages
from src.app.decorators.route_responses import handle_route_responses


router = APIRouter(prefix="/stages", tags=["stages"])

# Listado de etapas - ALL
@router.get("/get-all", response_model=List[StageOut])
@handle_route_responses(
    success_message=StagesMessages.OK_GET_ALL,
    error_message=StagesMessages.ERROR_GET_ALL,
)
async def get_all_projects(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=100, description="Número de elementos por página"),
    offset: int = Query(0, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(
        None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"
    ),
    filters: Optional[str] = Query(
        None,
        description="Criterios de filtrado en formato JSON (ej: {'name': '%john%', 'state': 0})",
    ),
) -> Dict[str, Any]:
    try:
        service = StageService(db)
        projects, total = await service.get_all(
            limit=limit, offset=offset, order_by=order_by, filters=filters
        )
        return paginated_response(projects, total, limit, offset)
    except Exception as e:
        raise e
    

# Crear etapas
@router.post("/create", response_model=StageCreate, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=StagesMessages.OK_CREATED,
    error_message=StagesMessages.ERROR_CREATED,
)
async def create_entity_type(
    data: StageCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = StageService(db)
        return await service.create(data.model_dump())
    except Exception as e:
        raise e

# Actualizar etapa
@router.put("/update/{stage_id}", response_model=StageOut)
@handle_route_responses(
    success_message=StagesMessages.OK_UPDATED,
    error_message=StagesMessages.ERROR_UPDATED,
    not_found_message=StagesMessages.ERROR_NOT_FOUND,
)
async def update_entity_type(
    stage_id: int, data: StageUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = StageService(db)
        return await service.update(stage_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise e

# Eliminar etapa
@router.delete("/delete/{stage_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=StagesMessages.OK_DELETED,
    error_message=StagesMessages.ERROR_DELETED,
    not_found_message=StagesMessages.ERROR_NOT_FOUND,
)
async def delete_project(stage_id: int, db: AsyncSession = Depends(get_db)) -> None:
    try:
        service = StageService(db)
        return await service.delete(stage_id)
    except Exception as e:
        raise e


#Listado de etapa por id
@router.get("/get-by-id/{stage_id}", response_model=StageOut)
@handle_route_responses(
    success_message=StagesMessages.OK_GET,
    error_message=StagesMessages.ERROR_GET,
    not_found_message=StagesMessages.ERROR_NOT_FOUND,
)
async def get_stage_by_id(
    stage_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = StageService(db)
        return await service.get_by_id(stage_id)
    except Exception as e:
        raise e

