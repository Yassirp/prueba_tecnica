from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.user_module.models.users import User
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.future import select

class UserRepository(BaseRepository[User]):
    def __init__(self, model: type[User], db_session: AsyncSession):
        super().__init__(model, db_session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalars().first()