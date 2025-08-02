from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.modules.roles_service import database
from app.modules.roles_service.schemas.rol_schemas import RolCreate, RolOut, PermisoCreate, PermisoOut
from app.modules.roles_service.repositories.rol_repository import crear_rol, listar_roles, crear_permiso, listar_permisos, asignar_permiso_a_rol

from fastapi import APIRouter

router = APIRouter(tags=["roles"])

@router.post("/", response_model=RolOut)
def crear_rol_endpoint(rol: RolCreate, db: Session = Depends(database.get_db)):
    return crear_rol(db, rol)

@router.get("/", response_model=list[RolOut])
def listar_roles_endpoint(db: Session = Depends(database.get_db)):
    return listar_roles(db)

@router.post("/permisos", response_model=PermisoOut)
def crear_permiso_endpoint(permiso: PermisoCreate, db: Session = Depends(database.get_db)):
    return crear_permiso(db, permiso)

@router.get("/permisos", response_model=list[PermisoOut])
def listar_permisos_endpoint(db: Session = Depends(database.get_db)):
    return listar_permisos(db)

@router.post("/{rol_id}/permisos/{permiso_id}")
def asignar_permiso_endpoint(rol_id: int, permiso_id: int, db: Session = Depends(database.get_db)):
    return asignar_permiso_a_rol(db, rol_id, permiso_id) 