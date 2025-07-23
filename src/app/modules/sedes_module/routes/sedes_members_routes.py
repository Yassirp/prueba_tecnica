from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.modules.sedes_module.schemas.sedes_members_schemas import SedesMemberCreate, SedesMemberUpdate, SedesMemberOut
from src.app.modules.sedes_module.services.sedes_members_services import SedesMemberService
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.shared.constants.messages import SedeMessages

router = APIRouter(prefix="/sede-members", tags=["Sedes Members"]) 

@router.get("/all", response_model=List[SedesMemberOut], status_code=status.HTTP_200_OK)
async def get_sedes_members(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = SedesMemberService(db)
    sedes, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(sedes, total, limit, offset)
    return http_response(message=SedeMessages.OK_GET_ALL, data=data)

@router.get("/{sede_id}", response_model=SedesMemberOut, status_code=status.HTTP_200_OK)
async def get_sede_with_relations(sede_id: int, db: AsyncSession = Depends(get_db)):
    service = SedesMemberService(db)
    sede = await service.get_by_id(sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_GET, data={"sede": sede})


@router.post("/create", response_model=SedesMemberOut, status_code=status.HTTP_201_CREATED)
async def create_sede_member(data: SedesMemberCreate, db: AsyncSession = Depends(get_db)):
    service = SedesMemberService(db)
    sede_member = await service.create(data)
    return http_response(message=SedeMessages.OK_CREATED, data={"sede_member": sede_member})

@router.post("/create-massive", response_model=List[SedesMemberOut], status_code=status.HTTP_201_CREATED)
async def create_sede_members(data: List[SedesMemberCreate], db: AsyncSession = Depends(get_db)):
    service = SedesMemberService(db)
    sede_members = []
    for member in data:
        sede_member = await service.create(member)
        sede_members.append(sede_member)
    return http_response(message=SedeMessages.OK_CREATED, data={"sede_members": sede_members})

@router.put("/{sede_member_id}", response_model=SedesMemberOut, status_code=status.HTTP_200_OK)
async def update_sede_member(sede_member_id: int, data: SedesMemberUpdate, db: AsyncSession = Depends(get_db)):
    service = SedesMemberService(db)
    updated_sede_member = await service.update(sede_member_id, data)
    if not updated_sede_member:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_UPDATED, data={"sede_member": updated_sede_member})

@router.delete("/{sede_member_id}", status_code=status.HTTP_200_OK)
async def delete_sede_member(sede_member_id: int, db: AsyncSession = Depends(get_db)):
    service = SedesMemberService(db)
    deleted = await service.delete(sede_member_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_DELETED, data=None)
