from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.modules.living_group_module.schemas.living_group_schemas import LivingGroupCreate, LivingGroupUpdate, LivingGroupOut, LivingGroupOutRelations
from src.app.modules.living_group_module.services.living_group_service import LivingGroupService
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.shared.constants.messages import GroupMessages

router = APIRouter(prefix="/living-groups", tags=["Living Groups"])

@router.get("/all", response_model=List[LivingGroupOut], status_code=status.HTTP_200_OK)
async def get_living_groups(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = LivingGroupService(db)
    living_groups, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(living_groups, total, limit, offset)
    return http_response(message=GroupMessages.OK_GET_ALL, data=data)

@router.get("/all-relationship", response_model=List[LivingGroupOutRelations], status_code=status.HTTP_200_OK)
async def get_living_groups_with_relations(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = LivingGroupService(db)
    living_groups, total = await service.get_all_with_relations(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(living_groups, total, limit, offset)
    return http_response(message=GroupMessages.OK_GET_ALL, data=data)

@router.post("/create", response_model=LivingGroupOut, status_code=status.HTTP_201_CREATED)
async def create_living_group(data: LivingGroupCreate, db: AsyncSession = Depends(get_db)):
    service = LivingGroupService(db)
    living_group = await service.create(data.model_dump())
    return http_response(message=GroupMessages.OK_CREATED, data=living_group)

@router.get("/{living_group_id}", response_model=LivingGroupOut, status_code=status.HTTP_200_OK)
async def get_living_group(living_group_id: int, db: AsyncSession = Depends(get_db)):
    service = LivingGroupService(db)
    living_group = await service.get_by_id(living_group_id)
    if not living_group:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_GET, data=living_group)

@router.get("/{living_group_id}/relationship", response_model=LivingGroupOutRelations, status_code=status.HTTP_200_OK)
async def get_living_group_with_relations(living_group_id: int, db: AsyncSession = Depends(get_db)):
    service = LivingGroupService(db)
    living_group = await service.get_by_id_with_relations(living_group_id)
    if not living_group:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    
    return http_response(message=GroupMessages.OK_GET, data=living_group)
@router.put("/{living_group_id}", response_model=LivingGroupOut, status_code=status.HTTP_200_OK)
async def update_living_group(living_group_id: int, data: LivingGroupUpdate, db: AsyncSession = Depends(get_db)):
    service = LivingGroupService(db)
    updated_living_group = await service.update(living_group_id, data.model_dump(exclude_unset=True))
    if not updated_living_group:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_UPDATED, data=updated_living_group)

@router.delete("/{living_group_id}", status_code=status.HTTP_200_OK)
async def delete_living_group(living_group_id: int, db: AsyncSession = Depends(get_db)):
    service = LivingGroupService(db)
    deleted = await service.delete(living_group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=GroupMessages.ERROR_NOT_FOUND)
    return http_response(message=GroupMessages.OK_DELETED, data=None)
