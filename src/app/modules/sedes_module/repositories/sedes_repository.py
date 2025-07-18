# Archivo generado automáticamente para sedes - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.sedes_module.models.sedes import Sede
from src.app.shared.bases.base_repository import BaseRepository

class SedeRepository(BaseRepository[Sede]):
    def __init__(self, model: type[Sede], db_session: AsyncSession):
        super().__init__(model, db_session)
        
    
    
