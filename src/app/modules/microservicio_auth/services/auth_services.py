from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.modules.microservicio_auth import database
from app.modules.microservicio_auth.models.auth_models import Usuario

load_dotenv()   

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Usamos APIKeyHeader para que Swagger solo muestre un campo para pegar el token
token_header = APIKeyHeader(name="Authorization")

# Función para verificar contraseña
def verificar_password(password_plano, password_hash):
    return bcrypt.verify(password_plano, password_hash)

# Crear token JWT
def crear_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Obtener usuario desde el token
def get_current_user(token: str = Depends(token_header), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # El token viene como "Bearer <token>", así que lo partimos
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Validar roles permitidos
def require_role(roles_permitidos: list[int]):
    def wrapper(current_user = Depends(get_current_user)):
        rol_usuario = current_user.roles_usuarios[0].rol_id if current_user.roles_usuarios else None
        if rol_usuario not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este recurso")
        return current_user
    return wrapper 