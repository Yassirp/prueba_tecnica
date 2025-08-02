from pydantic import BaseModel
from datetime import date, time

class ReservaBase(BaseModel):
    cancha_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time

class ReservaCreate(ReservaBase):
    pass

class ReservaOut(ReservaBase):
    id: int
    usuario_id: int
    estado: str

    class Config:
        from_attributes = True 