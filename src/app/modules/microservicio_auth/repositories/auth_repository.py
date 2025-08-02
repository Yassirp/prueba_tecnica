from sqlalchemy.orm import Session
from app.modules.microservicio_auth.schemas.auth_schemas import UsuarioCreate
from app.modules.microservicio_auth.models.auth_models import Usuario, RolUsuario
from passlib.hash import bcrypt

def crear_usuario(db: Session, usuario: UsuarioCreate, rol_id: int = 2):
    hashed_password = bcrypt.hash(usuario.password)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono,
        password=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    # Esto asigna rol al usuario
    rol_usuario = RolUsuario(usuario_id=db_usuario.id, rol_id=rol_id)
    db.add(rol_usuario)
    db.commit()

    return db_usuario


def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first() 