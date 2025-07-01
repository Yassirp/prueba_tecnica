from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.user_module.models.users import User
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.user_module.schemas.users_schemas import UserOut, ValidateLogin, AccessTokenOut, UserCreate, CodeVerification
from src.app.shared.security.jwt import create_access_token
from src.app.modules.user_module.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from fastapi import HTTPException, status
import random
from fastapi.responses import JSONResponse
from typing import Optional
import string

from src.app.shared.utils.request_utils import http_response
from src.app.shared.utils.service_token import send_email_token, send_sms_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserOut]):
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(User, db_session)
        super().__init__(
            model=User,
            repository_cls=UserRepository,
            db_session=db_session,
            out_schema=UserOut,
        )
        
        
        
    async def login(self, data: dict) -> AccessTokenOut:
        credentials = ValidateLogin(**data)
        user = await self.repository.get_by_email(credentials.email)

        if not user or not pwd_context.verify(credentials.password, str(user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrecta",
            )

        token = create_access_token(data={"sub": str(user.id)})
        return AccessTokenOut(access_token=token)
    
    
    async def register(self, data: dict) -> JSONResponse:
        # Validar que el email sea único
        existing_user = await self.repository.get_by_email(data["email"])
        if existing_user:
            return http_response(status=400, message="El email ya está registrado")
        
        data["state"] = 2  # Pendiente de aprobación
        validation_method = data.get("validation_method")  # "mail" o "cellphone"
        if not validation_method:
            return http_response(status=400, message="El metodo de validacion es requerido")
        
        # Generar código de 6 dígitos
        code = str(random.randint(100000, 999999))
        data["code"] = code
        data["password"] = pwd_context.hash(data["password"])

        if validation_method == "mail":
            response = await send_email_token(data["email"],"su codigo de verificacion es: " + code)
        elif validation_method == "cellphone":
            response = await send_sms_token(data["phone"], code)
        else:
            return http_response(status=400, message="Método de validación inválido")

        if response["status"] != "success":
            return http_response(status=500, message=response["message"], data=response.get("details"))

        user = UserCreate(**data)
        new_user = await self.repository.create(user.model_dump())

        return http_response(
            message="Usuario registrado correctamente",
            data={"code": code, "user": new_user, "validation_method": validation_method}
        )
    
    async def verify_user_code(self, data: CodeVerification) -> JSONResponse:

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
    
    async def update(self, entity_id: int, data: dict) -> Optional[dict]:
        # Validar que el email sea único si se está actualizando
        if "email" in data:
            existing_user = await self.repository.get_by_email(data["email"])
            if existing_user is not None:
                # Verificar si el usuario encontrado es diferente al que se está actualizando
                existing_id = getattr(existing_user, 'id', None)
                if existing_id is not None and existing_id != entity_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El email ya está registrado por otro usuario"
                    )
        
        # Si se está actualizando la contraseña, hashearla
        if "password" in data:
            data["password"] = pwd_context.hash(data["password"])
        
        updated_user = await self.repository.update(entity_id, data)
        if updated_user:
            return self.out_schema.model_validate(updated_user).model_dump()
        return None
    
    
    async def create_user(self, data: dict) -> JSONResponse:
        # 1. Generar contraseña aleatoria
        password_length = 10
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
        
        # 2. Hashear la contraseña y asignarla
        data['password'] = pwd_context.hash(random_password)
        
        if "role_id" not in data:
            data["role_id"] = 2
            
            
        user = UserCreate(**data)
        new_user = await self.repository.create(user.model_dump())
        
        # 3. Enviar la contraseña por correo
        await send_email_token(data['email'], f"Su contraseña temporal es: {random_password}", subject="Contraseña temporal")
        
        # 4. Retornar respuesta
        return http_response(
            message="Usuario creado correctamente. Se ha enviado la contraseña por correo electrónico.",
            data={"user": new_user}
        )