from sqlalchemy.orm import Session
from app.modules.reservas_services.schemas.reserva_schemas import ReservaCreate
from app.modules.reservas_services.models.reserva_models import Reserva

def crear_reserva(db: Session, reserva: ReservaCreate, usuario_id: int):
    nueva_reserva = Reserva(
        usuario_id=usuario_id,
        cancha_id=reserva.cancha_id,
        fecha=reserva.fecha,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        estado="activa"
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

def listar_reservas(db: Session, usuario_id: int, es_admin: bool):
    if es_admin:
        return db.query(Reserva).all()
    return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()

def cancelar_reserva(db: Session, reserva_id: int, usuario_id: int, es_admin: bool):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        return None
    if not es_admin and reserva.usuario_id != usuario_id:
        return False
    reserva.estado = "cancelada"
    db.commit()
    return reserva 