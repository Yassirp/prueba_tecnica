from typing import AsyncSession
from ....shared.bases.base_service import BaseService
from ..models.projects import Project
from ..repositories.projects_repository import ProjectRepository
from ..schemas.projects_schemas import ProjectCreate, ProjectUpdate

class ProjectService(BaseService):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Project,
            repository_cls=ProjectRepository,
            create_schema=ProjectCreate,
            update_schema=ProjectUpdate,
            db_session=db_session
        )
