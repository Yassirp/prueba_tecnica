# Archivo generado automáticamente para event - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.event_module.models.groups import Group
from src.app.modules.event_module.repositories.group_repository import GroupRepository
from src.app.modules.event_module.schemas.group_schemas import GroupOut

class GroupService(BaseService[Group, GroupOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Group,
            repository_cls=GroupRepository,
            db_session=db_session,
            out_schema=GroupOut,
        )
