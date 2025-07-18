from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.ubication_module.models.departments import Department
from src.app.shared.bases.base_repository import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db_session: AsyncSession, model: type[Department] = Department):
        super().__init__(model, db_session)