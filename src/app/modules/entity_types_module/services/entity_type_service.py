from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional, Any, cast
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.app.shared.bases.base_service import BaseService
from src.app.modules.entity_types_module.models.entity_types import EntityType
from src.app.modules.entity_types_module.repositories.entity_types_repository import (
    EntityTypeRepository,
)
from src.app.modules.entity_types_module.schemas.entity_types_schemas import EntityTypeOut
from src.app.modules.projects_module.services.projects_service import ProjectService
from src.app.shared.constants.project_enum import Setting

class EntityTypeService(BaseService[EntityType, EntityTypeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=EntityType,
            repository_cls=EntityTypeRepository,
            db_session=db_session,
            out_schema=EntityTypeOut,
        )
        self.project_service = ProjectService(db_session)
        self.db_session = db_session

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        project_id: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.project)
                ).where(self.model.state == Setting.STATUS.value)
            
            # FIltramos por key
            if project_id:
                stmt = stmt.where(self.model.project_id == project_id)

            # Aquí puedes aplicar filtros, orden y paginación si los necesitas.
            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)
            
            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()

            # Opcional: Si tienes filtros aplicados en SQL puedes contar antes,
            # si no, simplemente haces len().
            total = len(items)
            return items, total
        except Exception as e:
            raise e
    async def _validate_project_exists(self, project_id: int) -> None:
        try: 
            project = await self.project_service.get_by_id(project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'",
            )
        except Exception as e:
            raise e


    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            project_id = cast(int, data.get("project_id"))
            await self._validate_project_exists(project_id)

            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e

    async def update(
        self, entity_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            project_id = cast(int, data.get("project_id"))
            await self._validate_project_exists(project_id)

            item = await self.repo.update(entity_id, data)
            if not item:
                return None
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e

