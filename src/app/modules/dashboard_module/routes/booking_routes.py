from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.config.database.session import get_db
from app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from typing import Dict, Optional
from app.modules.dashboard_module.services.booking_services import BookingService
from app.modules.dashboard_module.schemas.booking_schemas import BookingCreate, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/all", status_code=status.HTTP_200_OK)
def get_bookings(db: Session = Depends(get_db),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Número de elementos por página"
    ),
    offset: Optional[int] = Query(
        None, ge=0, description="Número de elementos a omitir"
    ),
    order_by: Optional[str] = Query(
        None, description="Campo para ordenar (ej: 'id:asc' o 'date:desc')"
    ),
    filters: Dict[str, str] = Depends(get_filter_params)):
    service = BookingService(db)
    register, total = service.get_all(
        limit=limit or 10,
        offset=offset or 0, 
        order_by=order_by or 'id:asc', 
        filters=filters
    )
    paginate_ = paginated_response(register, total, limit or 10, offset or 0)
    return http_response(message="Reservas obtenidas correctamente", data=paginate_)

@router.get("/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    booking = service.get_by_id(booking_id)
    return http_response(message="Reserva obtenida correctamente", data=booking)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    service = BookingService(db)
    booking = service.create(data.model_dump())
    return http_response(message="Reserva creada correctamente", data=booking)

@router.put("/{booking_id}", status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db)):
    service = BookingService(db)
    booking = service.update(booking_id, data.model_dump(exclude_unset=True))
    return http_response(message="Reserva actualizada correctamente", data=booking)

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    service.delete(booking_id)
    return http_response(message="Reserva eliminada correctamente") 