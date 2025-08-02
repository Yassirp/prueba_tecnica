from fastapi import APIRouter, Depends, status,  Query
from sqlalchemy.orm import Session
from app.config.database.session import get_db
from app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from app.modules.soccer_field_module.services.soccer_field_services import SoccerFieldService
from app.modules.soccer_field_module.schemas.soccer_field_schemas import SoccerFieldCreate, SoccerFieldUpdate
from typing import Dict, Optional

router = APIRouter(prefix="/soccer_field", tags=["Soccer Field"])

@router.get("/all", status_code=status.HTTP_200_OK)
def get_soccer_fields(db: Session = Depends(get_db),
    # current_user = Depends(require_role([2])),  # Comentado temporalmente
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
    service = SoccerFieldService(db)
    register, total= service.get_all(
        limit=limit or 10,
        offset=offset or 0, 
        order_by=order_by or 'id:asc', 
        filters=filters
    )
    paginate_ =  paginated_response(register,total,limit or 10,offset or 0)
    return http_response(message="Canchas obtenidas correctamente", data=paginate_)

@router.get("/{soccer_field_id}", status_code=status.HTTP_200_OK)
def get_soccer_field(soccer_field_id: int, db: Session = Depends(get_db)):
    service = SoccerFieldService(db)
    soccer_field = service.get_by_id(soccer_field_id)
    return http_response(message="Cancha obtenida correctamente", data=soccer_field)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_soccer_field(data: SoccerFieldCreate, db: Session = Depends(get_db)):
    service = SoccerFieldService(db)
    soccer_field = service.create(data.model_dump())
    return http_response(message="Cancha creada correctamente", data=soccer_field)

@router.put("/{soccer_field_id}", status_code=status.HTTP_200_OK)
def update_soccer_field(soccer_field_id: int, data: SoccerFieldUpdate, db: Session = Depends(get_db)):
    service = SoccerFieldService(db)
    soccer_field = service.update(soccer_field_id, data.model_dump(exclude_unset=True))
    return http_response(message="Cancha actualizada correctamente", data=soccer_field)

@router.delete("/{soccer_field_id}", status_code=status.HTTP_200_OK)
def delete_soccer_field(soccer_field_id: int, db: Session = Depends(get_db)):
    service = SoccerFieldService(db)
    service.delete(soccer_field_id)
    return http_response(message="Cancha eliminada correctamente")



