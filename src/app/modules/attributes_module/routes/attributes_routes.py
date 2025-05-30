from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.attributes_module.schemas.attributes_schemas import( 
    AttributeCreate, 
    AttributeOut,
    AttributeUpdate
    )
from src.app.modules.attributes_module.services.attributes_service import AttributeService
from src.app.shared.constants.messages import AttributeMessages
from src.app.shared.utils.request_utils import paginated_response
from src.app.decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/attributes", tags=["Attribute"])


@router.get("/get-all", response_model=List[AttributeOut])
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
    id: Optional[int] = Query(None),
    parameter_id: Optional[int] = Query(None),
) -> Dict[str, Any]:
    try:
        service = AttributeService(db)
        attributes, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters,id=id,parameter_id=parameter_id
        )
        return paginated_response(attributes, total, limit, offset)
    except Exception as e:
        raise e
    
@router.get("/get-by-id/{attribute_id}", response_model=AttributeOut)
@handle_route_responses(
    success_message=AttributeMessages.OK_GET,
    error_message=AttributeMessages.ERROR_GET,
    not_found_message=AttributeMessages.ERROR_NOT_FOUND,
)
async def get_attribute_by_id(
    attribute_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = AttributeService(db)
        return await service.get_by_id(attribute_id)
    except Exception as e:
        raise e

@router.post("/create", response_model=AttributeOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=AttributeMessages.OK_CREATED,
    error_message=AttributeMessages.ERROR_CREATED,
)
async def create_parameter(
    data: AttributeCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:    
        service = AttributeService(db)
        return await service.create(data.model_dump())
    except Exception as e:
        raise e
    

@router.put("/update/{attribute_id}", response_model=AttributeOut)
@handle_route_responses(
    success_message=AttributeMessages.OK_UPDATED,
    error_message=AttributeMessages.ERROR_UPDATED,
    not_found_message=AttributeMessages.ERROR_NOT_FOUND,
)
async def update_attribute(
    attribute_id: int, data: AttributeUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:
        service = AttributeService(db)
        return await service.update(attribute_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise e
    

@router.delete("/delete/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=AttributeMessages.OK_DELETED,
    error_message=AttributeMessages.ERROR_DELETED,
    not_found_message=AttributeMessages.ERROR_NOT_FOUND,
)
async def delete_attribute(
    attribute_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    try:
        service = AttributeService(db)
        return await service.delete(attribute_id)
    except Exception as e: 
        raise e