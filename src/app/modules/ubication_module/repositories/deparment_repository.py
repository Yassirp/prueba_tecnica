from sqlalchemy.ext.asyncio import AsyncSession

from src.app.modules.ubication_module.models.countries import Country
from src.app.modules.ubication_module.models.departments import Department
from src.app.shared.bases.base_repository import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, model: type[Department], db_session: AsyncSession):
        super().__init__(model, db_session)