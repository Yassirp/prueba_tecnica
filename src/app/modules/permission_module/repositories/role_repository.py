from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.permission_module.models.role import Role
from src.app.shared.bases.base_repository import BaseRepository



class RoleRepository(BaseRepository[Role]):
    def __init__(self, model: type[Role], db_session: AsyncSession):
        super().__init__(model, db_session)
