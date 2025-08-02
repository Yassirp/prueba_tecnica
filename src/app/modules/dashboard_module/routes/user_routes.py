from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.config.database.session import get_db
from app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from typing import Dict, Optional
from app.modules.dashboard_module.services.user_services import UserService
from app.modules.dashboard_module.schemas.user_schemas import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/all", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Número de elementos por página"
    ),
    offset: Optional[int] = Query(
        None, ge=0, description="Número de elementos a omitir"
    ),
    order_by: Optional[str] = Query(
        None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"
    ),
    filters: Dict[str, str] = Depends(get_filter_params)):
    service = UserService(db)
    register, total = service.get_all(
        limit=limit or 10,
        offset=offset or 0, 
        order_by=order_by or 'id:asc', 
        filters=filters
    )
    paginate_ = paginated_response(register, total, limit or 10, offset or 0)
    return http_response(message="Usuarios obtenidos correctamente", data=paginate_)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_by_id(user_id)
    return http_response(message="Usuario obtenido correctamente", data=user)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.create(data.model_dump())
    return http_response(message="Usuario creado correctamente", data=user)

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.update(user_id, data.model_dump(exclude_unset=True))
    return http_response(message="Usuario actualizado correctamente", data=user)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete(user_id)
    return http_response(message="Usuario eliminado correctamente") 