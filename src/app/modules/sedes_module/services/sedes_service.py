# Archivo generado automáticamente para sedes - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.sedes_module.models.sedes import Sede
from src.app.modules.sedes_module.repositories.sedes_repository import SedeRepository
from src.app.modules.sedes_module.schemas.sedes_schemas import SedeOut

class SedeService(BaseService[Sede, SedeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Sede,
            repository_cls=SedeRepository,
            db_session=db_session,
            out_schema=SedeOut,
        )
