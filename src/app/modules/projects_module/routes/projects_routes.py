from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.modules.projects_module.services.projects_service import ProjectService
from app.modules.projects_module.schemas.projects_schemas import ProjectCreate, ProjectUpdate, ProjectOut
from app.config.database.session import get_db
from app.shared.utils.request_utils import paginated_response

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
async def get_all_projects(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    order_by: Optional[str] = Query(None),
    filters: Optional[str] = Query(None)  # Si pasas filtros personalizados, puedes hacer parseo aquí
):
    service = ProjectService(db)
    projects, total = await service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
    return paginated_response(projects, total, limit, offset)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.create(data.model_dump())

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    updated_project = await service.update(project_id, data.model_dump(exclude_unset=True))
    if not updated_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return updated_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    deleted = await service.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
