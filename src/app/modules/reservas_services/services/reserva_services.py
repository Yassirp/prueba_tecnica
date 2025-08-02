from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

token_header = APIKeyHeader(name="Authorization")

def get_current_user(token: str = Depends(token_header)):
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        rol_id: int = payload.get("rol_id")
        if email is None or rol_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"email": email, "rol_id": rol_id}

def require_role(roles_permitidos: list[int]):
    def wrapper(current_user = Depends(get_current_user)):
        if current_user["rol_id"] not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este recurso")
        return current_user
    return wrapper 