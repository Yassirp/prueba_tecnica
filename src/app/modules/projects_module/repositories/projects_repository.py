from sqlalchemy.ext.asyncio import AsyncSession
from ..models.projects import Project
from ....shared.bases.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)
