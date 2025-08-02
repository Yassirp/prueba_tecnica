from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.dashboard_module.models.users import User
from app.shared.bases.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, model: type[User], db_session: AsyncSession):
        super().__init__(model, db_session) 