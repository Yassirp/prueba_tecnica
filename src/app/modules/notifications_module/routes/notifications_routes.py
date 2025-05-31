# Archivo generado autom�ticamente para notifications - routes
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.notifications_module.schemas.notifications_schemas import (
    NotificationCreate,
    NotificationUpdate,
    NotificationOut
)
from src.app.modules.notifications_module.services.notifications_service import NotificationsService
from src.app.shared.utils.request_utils import paginated_response
from src.app.shared.constants.messages import NotificationMessages
from src.app.decorators.route_responses import handle_route_responses
from typing import Optional

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/get-all-notifications", response_model=list[NotificationOut])
@handle_route_responses(
    success_message=NotificationMessages.OK_GET_ALL,
    error_message=NotificationMessages.ERROR_GET_ALL,
    not_found_message=NotificationMessages.ERROR_NOT_FOUND,
)
# Obtener todas las notificaciones
async def get_all_notifications(
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
):
    try:
        service = NotificationsService(db)
        notifications, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
        return paginated_response(notifications, total, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get-notification-by-id/{notification_id}", response_model=NotificationOut)
@handle_route_responses(
    success_message=NotificationMessages.OK_GET,
    error_message=NotificationMessages.ERROR_GET,
    not_found_message=NotificationMessages.ERROR_NOT_FOUND,
)
# Obtener una notificación por su ID
async def get_notification_by_id(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        service = NotificationsService(db)
        notification = await service.get_by_id(notification_id)
        return notification
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   

@router.post("/create-notification", response_model=NotificationOut)
@handle_route_responses(
    success_message=NotificationMessages.OK_CREATED,
    error_message=NotificationMessages.ERROR_CREATED,
    not_found_message=NotificationMessages.ERROR_NOT_FOUND,
)
# Crear una notificación
async def create_notification(
    notification: NotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        service = NotificationsService(db)
        notification = await service.create(notification.model_dump())
        return notification
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update-notification/{notification_id}", response_model=NotificationOut)
@handle_route_responses(
    success_message=NotificationMessages.OK_UPDATED,
    error_message=NotificationMessages.ERROR_UPDATED,
    not_found_message=NotificationMessages.ERROR_NOT_FOUND,
)

async def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        service = NotificationsService(db)
        notification = await service.update(notification_id, notification.model_dump())
        return notification
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
