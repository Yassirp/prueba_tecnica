from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.modules.living_group_module.schemas.living_group_user_schemas import LivingGroupUserCreate, LivingGroupUserUpdate, LivingGroupUserOut
from src.app.modules.living_group_module.services.living_group_user_service import LivingGroupUserService
from src.app.shared.constants.messages import LivingGroupUserMessages

router = APIRouter(prefix="/living-groups/user", tags=["Living Groups Users"])


@router.get("/all", response_model=List[LivingGroupUserOut], status_code=status.HTTP_200_OK)
async def get_living_group_users(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = LivingGroupUserService(db)
    users, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(users, total, limit, offset)
    return http_response(message=LivingGroupUserMessages.OK_GET_ALL, data=data)

@router.get("/{user_id}", response_model=LivingGroupUserOut, status_code=status.HTTP_200_OK)
async def get_living_group_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = LivingGroupUserService(db)
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=LivingGroupUserMessages.ERROR_NOT_FOUND)
    return http_response(message=LivingGroupUserMessages.OK_GET, data={"living_group_user": user})

@router.post("/create", response_model=LivingGroupUserOut, status_code=status.HTTP_201_CREATED)
async def create_living_group_user(data: LivingGroupUserCreate, db: AsyncSession = Depends(get_db)):
    service = LivingGroupUserService(db)
    user = await service.create(data)
    return http_response(message=LivingGroupUserMessages.OK_CREATED, data={"living_group_user": user})

@router.post("/create-massive", response_model=List[LivingGroupUserOut], status_code=status.HTTP_201_CREATED)
async def create_living_group_user_massive(data: List[LivingGroupUserCreate], db: AsyncSession = Depends(get_db)):
    service = LivingGroupUserService(db)
    users = []
    for user in data:  
        users.append(await service.create(user))
    return http_response(message=LivingGroupUserMessages.OK_CREATED, data={"living_group_users": users})

@router.put("/{user_id}", response_model=LivingGroupUserOut, status_code=status.HTTP_200_OK)
async def update_living_group_user(user_id: int, data: LivingGroupUserUpdate, db: AsyncSession = Depends(get_db)):
    service = LivingGroupUserService(db)
    updated_user = await service.update(user_id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail=LivingGroupUserMessages.ERROR_NOT_FOUND)
    return http_response(message=LivingGroupUserMessages.OK_UPDATED, data={"living_group_user": updated_user})

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_living_group_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = LivingGroupUserService(db)
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=LivingGroupUserMessages.ERROR_NOT_FOUND)
    return http_response(message=LivingGroupUserMessages.OK_DELETED, data=None)