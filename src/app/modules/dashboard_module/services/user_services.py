from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.bases.base_service import BaseService
from app.modules.dashboard_module.models.users import User
from app.modules.dashboard_module.repositories.user_repository import UserRepository
from app.modules.dashboard_module.schemas.user_schemas import UserOut

class UserService(BaseService[User, UserOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = UserRepository(User, self.db_session)
        super().__init__(
            model=User,
            repository_cls=UserRepository,
            db_session=self.db_session,
            out_schema=UserOut,
        ) 