from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.modules.reservas_services import database
from app.modules.reservas_services.models.reserva_models import Reserva
from app.modules.reservas_services.schemas.reserva_schemas import ReservaCreate, ReservaOut
from app.modules.reservas_services.repositories.reserva_repository import crear_reserva, listar_reservas, cancelar_reserva
from app.modules.reservas_services.services.reserva_services import get_current_user
# Nota: Para obtener el usuario real, necesitarías hacer una llamada al microservicio de auth
# Por ahora usamos el email del token como identificador

from fastapi import APIRouter

router = APIRouter(tags=["reservas"])

@router.post("/", response_model=ReservaOut)
def crear_reserva_endpoint(
    reserva: ReservaCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    # Por ahora usamos el email como identificador del usuario
    # En un entorno real, harías una llamada al microservicio de auth
    return crear_reserva(db, reserva, usuario_id=1)  # ID temporal

@router.get("/", response_model=list[ReservaOut])
def listar_reservas_endpoint(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    es_admin = current_user["rol_id"] == 2
    return listar_reservas(db, usuario_id=current_user["email"], es_admin=es_admin)

@router.delete("/{reserva_id}")
def cancelar_reserva_endpoint(
    reserva_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    es_admin = current_user["rol_id"] == 2
    resultado = cancelar_reserva(db, reserva_id, usuario_id=current_user["email"], es_admin=es_admin)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if resultado is False:
        raise HTTPException(status_code=403, detail="No puedes cancelar esta reserva")
    return {"mensaje": "Reserva cancelada"} 