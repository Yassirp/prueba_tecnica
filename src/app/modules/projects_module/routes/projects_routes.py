from fastapi import APIRouter, Depends, Query, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from ....config.database.session import get_db
from ..services.projects_service import ProjectService
from ..schemas.projects_schemas import ProjectCreate, ProjectUpdate, ProjectOut
from ....shared.utils.request_utils import paginated_response
from ....shared.constants.messages import ProjectsMessages
from ....decorators.route_responses import handle_route_responses

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
@handle_route_responses(
    success_message=ProjectsMessages.OK_GET_ALL,
    error_message=ProjectsMessages.ERROR_GET_ALL
)
async def get_all_projects(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=100, description="Número de elementos por página"),
    offset: int = Query(0, ge=0, description="Número de elementos a omitir"),
    order_by: Optional[str] = Query(None, description="Campo para ordenar (ej: 'id:asc' o 'name:desc')"),
    filters: Optional[str] = Query(None, description="Criterios de filtrado en formato JSON (ej: {name: '%john%', state: 0})")
):
    service = ProjectService(db)
    projects, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    return paginated_response(projects, total, limit, offset)


@router.get("/{project_id}", response_model=ProjectOut)
@handle_route_responses(
    success_message=ProjectsMessages.OK_GET,
    error_message=ProjectsMessages.ERROR_GET,
    not_found_message=ProjectsMessages.ERROR_NOT_FOUND
)
async def get_project_by_id(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.get_by_id(project_id)


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=ProjectsMessages.OK_CREATED,
    error_message=ProjectsMessages.ERROR_CREATED
)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.create(data.model_dump())


@router.put("/{project_id}", response_model=ProjectOut)
@handle_route_responses(
    success_message=ProjectsMessages.OK_UPDATED,
    error_message=ProjectsMessages.ERROR_UPDATED,
    not_found_message=ProjectsMessages.ERROR_NOT_FOUND
)
async def update_project(project_id: int, data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.update(project_id, data.model_dump(exclude_unset=True))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_route_responses(
    success_message=ProjectsMessages.OK_DELETED,
    error_message=ProjectsMessages.ERROR_DELETED,
    not_found_message=ProjectsMessages.ERROR_NOT_FOUND
)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.delete(project_id)
