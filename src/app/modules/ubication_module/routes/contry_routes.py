from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.ubication_module.schemas.country_schemas import CountryCreate, CountryUpdate
from src.app.modules.ubication_module.services.country_services import CountryService
from typing import Dict
from src.app.shared.utils.request_utils import  http_response, get_filter_params, paginated_response
from src.app.middleware.api_auth import require_auth, User 


router = APIRouter(prefix="/country", tags=["Country"])


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_countries(db: AsyncSession = Depends(get_db),

    filters: Dict[str, str] = Depends(get_filter_params)):
    service = CountryService(db)
    register, total= await service.get_all_countries(limit=10,offset=0, order_by="id:asc", filters=filters)
    paginate_ =  paginated_response(register,total,limit=10,offset=0)
    return http_response(message="Países obtenidos correctamente", data=paginate_)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_relationship(
    data: dict,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = CountryService(db)
    try:
        validated_data = CountryCreate(**data)
        country=  await service.create(validated_data.model_dump())
        return http_response(message="País creado correctamente", data=country)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user_relationship(
    id: int,
    data: CountryUpdate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = CountryService(db)
    country = await service.update(id, data.model_dump())
    return http_response(message="País actualizado correctamente", data=country)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_relationship(
    id: int,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = CountryService(db)
    await service.delete(id)
    return http_response(message="País eliminado correctamente")

