
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.user_module.models.users import User
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.user_module.schemas.users_schemas import UserOut, ValidateLogin, AccessTokenOut
from src.app.shared.security.jwt import create_access_token
from src.app.modules.user_module.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from fastapi import HTTPException, status

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