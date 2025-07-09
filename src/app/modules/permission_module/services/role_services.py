from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.permission_module.models.role import Role
from src.app.modules.permission_module.repositories.role_repository import RoleRepository
from src.app.modules.permission_module.schemas.role_schema import RoleOut
from src.app.shared.bases.base_service import BaseService

class RoleService(BaseService[Role, RoleOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Role,
            repository_cls=RoleRepository,
            db_session=db_session,
            out_schema=RoleOut,
        )
        