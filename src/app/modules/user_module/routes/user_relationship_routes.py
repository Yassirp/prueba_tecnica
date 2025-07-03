from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.schemas.users_relationship_schemas import UserRelationshipCreate, UserRelationshipUpdate
from src.app.modules.user_module.services.user_relationship_service import UserRelationshipService
from typing import List
from src.app.shared.utils.request_utils import get_filter_params, paginated_response, http_response
from src.app.middleware.api_auth import require_auth, User 


router = APIRouter(prefix="/user-relationship", tags=["User Relationship"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_relationship(
    data: dict,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = UserRelationshipService(db)
    try:
        validated_data = UserRelationshipCreate(**data)
        user_relationship=  await service.create(validated_data.model_dump())
        return http_response(message="Relación creada correctamente", data=user_relationship)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/create-massive", status_code=status.HTTP_201_CREATED)
async def create_user_relationship_massive(
    data: List[dict],
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = UserRelationshipService(db)
    data_list = []
    try:
        for item in data:
            await service.create(item)
            data_list.append(item)
        return http_response(message="Relaciones creadas correctamente", data={"items": data_list})   
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_user_relationship(
    id: int,
    data: UserRelationshipUpdate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    service = UserRelationshipService(db)
    return await service.update(id, data.model_dump())