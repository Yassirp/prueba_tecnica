# Archivo generado automáticamente para parameters - routes
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.parameters_module.schemas.parameters_schemas import (
    ParameterCreate,
    ParameterOut,
    ParameterUpdate
    )
from src.app.modules.parameters_module.services.parameters_service import ParameterService
from src.app.shared.constants.messages import AttributeMessages, ParameterMessages
from src.app.shared.utils.request_utils import paginated_response
from src.app.decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/parameters", tags=["Parameters"])


@router.get("/get-all", response_model=List[ParameterOut])
@handle_route_responses(
    success_message=ParameterMessages.OK_GET_ALL,
    error_message=ParameterMessages.ERROR_GET_ALL,
)
async def get_all_parameter(
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
    try:
        service = ParameterService(db)
        parameters, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters
        )
        return paginated_response(parameters, total, limit, offset)
    except Exception as e:
        raise e
    
@router.get("/get-by-id/{parameter_id}", response_model=ParameterOut)
@handle_route_responses(
    success_message=ParameterMessages.OK_GET,
    error_message=ParameterMessages.ERROR_GET,
    not_found_message=ParameterMessages.ERROR_NOT_FOUND,
)
async def get_parameter_by_id(
    parameter_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = ParameterService(db)
        return await service.get_by_id(parameter_id)
    except Exception as e:
        raise e
    
@router.post("/create", response_model=ParameterOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=ParameterMessages.OK_CREATED,
    error_message=ParameterMessages.ERROR_CREATED,
)
async def create_parameter(
    data: ParameterCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:    
        service = ParameterService(db)
        return await service.create(data.model_dump())
    except Exception as e:
        raise e
    
@router.put("/update/{parameter_id}", response_model=ParameterOut)
@handle_route_responses(
    success_message=ParameterMessages.OK_UPDATED,
    error_message=ParameterMessages.ERROR_UPDATED,
    not_found_message=ParameterMessages.ERROR_NOT_FOUND,
)
async def update_parameter(
    parameter_id: int, data: ParameterUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = ParameterService(db)
        return await service.update(parameter_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise e
    

@router.delete("/delete/{parameter_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=ParameterMessages.OK_DELETED,
    error_message=ParameterMessages.ERROR_DELETED,
    not_found_message=ParameterMessages.ERROR_NOT_FOUND,
)
async def delete_parameter(
    parameter_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    try:
        service = ParameterService(db)
        return await service.delete(parameter_id)
    except Exception as e: 
        raise e
    
@router.get("/get-all-attribute", response_model=List[ParameterOut])
@handle_route_responses(
    success_message=AttributeMessages.OK_GET_ALL,
    error_message=AttributeMessages.ERROR_GET_ALL,
)
async def get_all_attribute(
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
    try:
        service = ParameterService(db)
        attribiute, total = await service.get_all_attribute(
        limit=limit, offset=offset, order_by=order_by, filters=filters
        )
        return paginated_response(attribiute, total, limit, offset)
    except Exception as e:
        raise e