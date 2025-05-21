from typing import AsyncSession
from app.shared.bases.base_service import BaseService
from app.modules.ProjectsModule.models.projects import Project
from app.modules.ProjectsModule.repositories.projects_repository import ProjectRepository
from app.modules.ProjectsModule.schemas.projects_schemas import ProjectCreate, ProjectUpdate

class ProjectService(BaseService):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Project,
            repository_cls=ProjectRepository,
            create_schema=ProjectCreate,
            update_schema=ProjectUpdate,
            db_session=db_session
        )
