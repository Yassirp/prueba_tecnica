from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, Any, cast
from fastapi import HTTPException, status
from src.app.shared.bases.base_service import BaseService
from src.app.modules.entity_types_module.models.entity_types import EntityType
from src.app.modules.entity_types_module.repositories.entity_types_repository import (
    EntityTypeRepository,
)
from src.app.modules.entity_types_module.schemas.entity_type import EntityTypeOut
from src.app.modules.projects_module.services.projects_service import ProjectService

class EntityTypeService(BaseService[EntityType, EntityTypeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=EntityType,
            repository_cls=EntityTypeRepository,
            db_session=db_session,
            out_schema=EntityTypeOut,
        )
        self.project_service = ProjectService(db_session)

    async def _validate_project_exists(self, project_id: int) -> None:
        project = await self.project_service.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el proyecto con el id '{project_id}'",
            )

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        project_id = cast(int, data.get("project_id"))
        await self._validate_project_exists(project_id)

        item = await self.repo.create(data)
        return self.out_schema.model_validate(item).model_dump()

    async def update(
        self, entity_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        project_id = cast(int, data.get("project_id"))
        await self._validate_project_exists(project_id)

        item = await self.repo.update(entity_id, data)
        if not item:
            return None
        return self.out_schema.model_validate(item).model_dump()
