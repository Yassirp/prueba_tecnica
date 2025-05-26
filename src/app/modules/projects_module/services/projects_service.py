from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.projects_module.models.projects import Project
from src.app.modules.projects_module.repositories.projects_repository import (
    ProjectRepository,
)
from src.app.modules.projects_module.schemas.projects_schemas import ProjectOut


class ProjectService(BaseService[Project, ProjectOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Project,
            repository_cls=ProjectRepository,
            db_session=db_session,
            out_schema=ProjectOut,
        )