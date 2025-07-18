from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.modules.living_group_module.schemas.event_schemas import EventCreate, EventUpdate, EventOut
from src.app.modules.living_group_module.services.event_service import EventService
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.shared.constants.messages import EventMessages

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/all", response_model=List[EventOut], status_code=status.HTTP_200_OK)
async def get_events(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = EventService(db)
    events, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(events, total, limit, offset)
    return http_response(message=EventMessages.OK_GET_ALL, data=data)

@router.get("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    event = await service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=EventMessages.ERROR_NOT_FOUND)
    return http_response(message=EventMessages.OK_GET, data={"event": event})

@router.post("/create", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(data: EventCreate, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    event = await service.create(data.model_dump())
    return http_response(message=EventMessages.OK_CREATED, data={"event": event})

@router.put("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
async def update_event(event_id: int, data: EventUpdate, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    updated_event = await service.update(event_id, data.model_dump(exclude_unset=True))
    if not updated_event:
        raise HTTPException(status_code=404, detail=EventMessages.ERROR_NOT_FOUND)
    return http_response(message=EventMessages.OK_UPDATED, data={"event": updated_event})

@router.delete("/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    service = EventService(db)
    deleted = await service.delete(event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=EventMessages.ERROR_NOT_FOUND)
    return http_response(message=EventMessages.OK_DELETED, data=None) 