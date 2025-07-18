from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.modules.event_module.schemas.group_schemas import GroupCreate, GroupUpdate, GroupOut
from src.app.modules.event_module.services.group_service import GroupService
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.shared.constants.messages import GroupMessages

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/all", response_model=List[GroupOut], status_code=status.HTTP_200_OK)
async def get_groups(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = GroupService(db)
    groups, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(groups, total, limit, offset)
    return http_response(message=GroupMessages.OK_GET_ALL, data=data)

@router.get("/{group_id}", response_model=GroupOut, status_code=status.HTTP_200_OK)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    service = GroupService(db)
    group = await service.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_GET, data={"group": group})

@router.post("/create", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
async def create_group(data: GroupCreate, db: AsyncSession = Depends(get_db)):
    service = GroupService(db)
    group = await service.create(data.model_dump())
    return http_response(message=GroupMessages.OK_CREATED, data={"group": group})

@router.put("/{group_id}", response_model=GroupOut, status_code=status.HTTP_200_OK)
async def update_group(group_id: int, data: GroupUpdate, db: AsyncSession = Depends(get_db)):
    service = GroupService(db)
    updated_group = await service.update(group_id, data.model_dump(exclude_unset=True))
    if not updated_group:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_UPDATED, data={"group": updated_group})

@router.delete("/{group_id}", status_code=status.HTTP_200_OK)
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    service = GroupService(db)
    deleted = await service.delete(group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_DELETED, data=None)
