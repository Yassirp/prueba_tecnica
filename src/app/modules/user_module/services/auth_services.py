from src.app.modules.user_module.services.user_service import UserService
from src.app.modules.user_module.schemas.users_schemas import ValidateLogin, AccessTokenOut, CodeVerification
from src.app.shared.security.jwt import create_access_token
from fastapi import HTTPException, status
from datetime import datetime
from pytz import timezone
from passlib.context import CryptContext
from src.app.shared.utils.request_utils import http_response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService(UserService):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

    async def login(self, data: dict) -> AccessTokenOut:
        credentials = ValidateLogin(**data)
        user = await self.repository.get_by_email(credentials.email)

        if not user or not pwd_context.verify(credentials.password, str(user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrecta",
            )
            
        now_bogota = datetime.now(timezone("America/Bogota")).replace(tzinfo=None)
        await self.repository.update(user.id, {"last_login": now_bogota, "is_active": True})
        data_token = {
            "id": user.id, 
            "role_id": user.role_id, 
            "email": user.email,
            "name": user.name, 
            "last_name": user.last_name, 
            "phone": user.phone,
            "country_id": user.country_id, 
            "department_id": user.department_id,
            "municipality_id": user.municipality_id, 
            "address": user.address,
            "state": user.state, 
            "created_at": user.created_at.isoformat() if user.created_at is not None else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
            "deleted_at": user.deleted_at.isoformat() if user.deleted_at is not None else None
        }
            
        token = create_access_token(data=data_token)
        return AccessTokenOut(access_token=token)
    
    
    async def logout(self, user_id: int):
        await self.repository.update(user_id, {"is_active": False})
        return http_response(message="Usuario deslogueado correctamente")
    
    async def register(self, data: dict):
        pass

    async def verify_user_code(self, data: CodeVerification):

        user = await self.repository.get_by_id(data.user_id)
        print("user", user)
        if not user:
            return http_response(status=404, message="Usuario no encontrado")

        if str(user.code) != data.code:
            return http_response(status=400, message="Código incorrecto")


        await self.repository.update(user.id, {"state": 1})
        
        return http_response(
            message="Usuario verificado correctamente",
            data={"user": user}
        )
    