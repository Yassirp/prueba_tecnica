from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from src.app.shared.constants.settings import Settings

security = HTTPBearer()


class User:
    def __init__(self, id: int, role_id: int):
        self.id = id
        self.role_id = role_id


def get_fake_user() -> User:
    return User(id=2, role_id=1)


def get_user_from_token(token: str) -> User:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        role_id = int(payload.get("role_id", 0))

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return User(id=user_id, role_id=role_id)

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")


def set_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    if Settings.DEBUG:
        return get_fake_user()

    if not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    token = credentials.credentials
    return get_user_from_token(token)
