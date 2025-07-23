# Archivo generado automáticamente para sedes - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_repository import BaseRepository
from src.app.modules.sedes_module.models.sedes_members import SedesMember

class SedesMemberRepository(BaseRepository[SedesMember]):
    def __init__(self, model: type[SedesMember], db_session: AsyncSession):
        super().__init__(model, db_session)
        
        