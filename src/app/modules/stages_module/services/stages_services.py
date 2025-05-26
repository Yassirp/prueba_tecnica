from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, Any, cast
from fastapi import HTTPException, status
from src.app.modules.projects_module.models.projects import Project
from src.app.modules.stages_module.models.stages import Stage
from src.app.shared.bases.base_service import BaseService
from src.app.modules.stages_module.repositories.stages_repositories import (
    StageRepository
)
from src.app.modules.stages_module.schemas.stages_schemas import StageOut


class StageService(BaseService[Stage, StageOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Stage,
            repository_cls=StageRepository,
            db_session=db_session,
            out_schema=StageOut,
        )
        self.db_session = db_session

    async def _validate_project_exists(self, project_id: int) -> None:
        try:
            project = await self.db_session.get(Project, project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'",
                )
            return True
        except Exception as e:
            raise e
        
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            project_id = data.get("project_id")
            await self._validate_project_exists(project_id)

            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e
        
    
    async def update( self, stage_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            project_id =  data.get("project_id", None)
            await self._validate_project_exists(project_id)

            item = await self.repo.update(stage_id, data)
            if not item:
                return None
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e
