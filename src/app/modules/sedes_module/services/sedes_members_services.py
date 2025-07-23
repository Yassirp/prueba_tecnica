from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.sedes_module.models.sedes_members import SedesMember
from src.app.modules.sedes_module.repositories.sedes_members_repository import SedesMemberRepository
from src.app.modules.sedes_module.schemas.sedes_members_schemas import SedesMemberOut

class SedesMemberService(BaseService[SedesMember, SedesMemberOut]):
    def __init__(self, db_session: AsyncSession):   
        self.db_session = db_session
        super().__init__(
            model=SedesMember,
            repository_cls=SedesMemberRepository,
            db_session=db_session,
            out_schema=SedesMemberOut,
        )
