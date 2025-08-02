from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.modules.microservicio_auth import database
from app.modules.microservicio_auth.models.auth_models import Usuario, RolUsuario
from app.modules.microservicio_auth.schemas.auth_schemas import UsuarioCreate, UsuarioOut
from app.modules.microservicio_auth.repositories.auth_repository import crear_usuario, obtener_usuario_por_email
from app.modules.microservicio_auth.services.auth_services import verificar_password, crear_access_token, get_current_user

from fastapi import APIRouter

router = APIRouter(tags=["authentication"])

@router.post("/registro", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(database.get_db)):
    db_usuario = obtener_usuario_por_email(db, usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crear_usuario(db, usuario)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = obtener_usuario_por_email(db, form_data.username)
    if not user or not verificar_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Obtener el rol del usuario
    rol_usuario = db.query(RolUsuario).filter(RolUsuario.usuario_id == user.id).first()
    rol_id = rol_usuario.rol_id if rol_usuario else None

    access_token = crear_access_token(
        data={"sub": user.email, "rol_id": rol_id},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/perfil")
def perfil(usuario_actual = Depends(get_current_user)):
    return {"id": usuario_actual.id, "nombre": usuario_actual.nombre, "email": usuario_actual.email} 