from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.modules.reservas_services.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cancha_id = Column(Integer, ForeignKey("canchas.id"))
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(50), nullable=False, default="activa")
    fechareg = Column(DateTime, default=func.now())

    cancha = relationship("Cancha", back_populates="reservas") 