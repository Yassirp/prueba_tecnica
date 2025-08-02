from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolOut(RolBase):
    id: int
    class Config:
        from_attributes = True  # Pydantic v2

class PermisoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class PermisoCreate(PermisoBase):
    pass

class PermisoOut(PermisoBase):
    id: int
    class Config:
        from_attributes = True 