from sqlalchemy.ext.asyncio import AsyncSession
from ....shared.bases.base_service import BaseService
from ..models.projects import Project
from ..repositories.projects_repository import ProjectRepository
from ..schemas.projects_schemas import ProjectOut

class ProjectService(BaseService[Project, ProjectOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Project,
            repository_cls=ProjectRepository,
            db_session=db_session,
            out_schema=ProjectOut
        )