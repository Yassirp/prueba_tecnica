# Archivo generado automáticamente para parameters - routes
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.permission_module.schemas.role_schema import (
    RoleOut
    )
from src.app.modules.permission_module.services.role_services import RoleService
from src.app.shared.constants.messages import ParameterMessages
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.decorators.route_responses import handle_route_responses
from src.app.middleware.api_auth import require_auth, User

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/all", response_model=List[RoleOut])
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
    filters: Dict[str, str] = Depends(get_filter_params)
):
    try:
        service = RoleService(db)
        parameters, total = await service.get_all(
        limit=limit, offset=offset, order_by=order_by, filters=filters
        )
        data= paginated_response(parameters, total, limit, offset)
        return data
    except Exception as e:
        raise e
    