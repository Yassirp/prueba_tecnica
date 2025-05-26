from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_repository import BaseRepository
from src.app.modules.projects_module.models.projects import Project

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, model: type[Project], db_session: AsyncSession):
        super().__init__(model, db_session)
