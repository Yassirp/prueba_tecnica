from sqlalchemy.orm import Session
from app.modules.roles_service.schemas.rol_schemas import RolCreate, PermisoCreate
from app.modules.roles_service.models.rol_models import Rol, Permiso, RolPermiso

# CRUD Roles
def crear_rol(db: Session, rol: RolCreate):
    db_rol = Rol(nombre=rol.nombre, descripcion=rol.descripcion)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def listar_roles(db: Session):
    return db.query(Rol).all()

# CRUD Permisos
def crear_permiso(db: Session, permiso: PermisoCreate):
    db_permiso = Permiso(nombre=permiso.nombre, descripcion=permiso.descripcion)
    db.add(db_permiso)
    db.commit()
    db.refresh(db_permiso)
    return db_permiso

def listar_permisos(db: Session):
    return db.query(Permiso).all()

# Asignar permiso a rol
def asignar_permiso_a_rol(db: Session, rol_id: int, permiso_id: int):
    relacion = RolPermiso(rol_id=rol_id, permiso_id=permiso_id)
    db.add(relacion)
    db.commit()
    db.refresh(relacion)
    return relacion 