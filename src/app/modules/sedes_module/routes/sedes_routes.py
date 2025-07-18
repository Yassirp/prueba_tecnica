from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, List
from src.app.config.database.session import get_db
from src.app.modules.sedes_module.schemas.sedes_schemas import SedeCreate, SedeUpdate, SedeOut
from src.app.modules.sedes_module.services.sedes_service import SedeService
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.shared.constants.messages import SedeMessages

router = APIRouter(prefix="/sedes", tags=["Sedes"])

@router.get("/all", response_model=List[SedeOut], status_code=status.HTTP_200_OK)
async def get_sedes(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Número de elementos por página"),
    offset: Optional[int] = Query(None, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Dict[str, str] = Depends(get_filter_params)
):
    service = SedeService(db)
    sedes, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    data = paginated_response(sedes, total, limit, offset)
    return http_response(message=SedeMessages.OK_GET_ALL, data=data)

@router.get("/{sede_id}", response_model=SedeOut, status_code=status.HTTP_200_OK)
async def get_sede(sede_id: int, db: AsyncSession = Depends(get_db)):
    service = SedeService(db)
    sede = await service.get_by_id(sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_GET, data={"sede": sede})

@router.post("/create", response_model=SedeOut, status_code=status.HTTP_201_CREATED)
async def create_sede(data: SedeCreate, db: AsyncSession = Depends(get_db)):
    service = SedeService(db)
    sede = await service.create(data.model_dump())
    return http_response(message=SedeMessages.OK_CREATED, data={"sede": sede})

@router.put("/{sede_id}", response_model=SedeOut, status_code=status.HTTP_200_OK)
async def update_sede(sede_id: int, data: SedeUpdate, db: AsyncSession = Depends(get_db)):
    service = SedeService(db)
    updated_sede = await service.update(sede_id, data.model_dump(exclude_unset=True))
    if not updated_sede:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_UPDATED, data={"sede": updated_sede})

@router.delete("/{sede_id}", status_code=status.HTTP_200_OK)
async def delete_sede(sede_id: int, db: AsyncSession = Depends(get_db)):
    service = SedeService(db)
    deleted = await service.delete(sede_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=SedeMessages.ERROR_NOT_FOUND)
    return http_response(message=SedeMessages.OK_DELETED, data=None)
