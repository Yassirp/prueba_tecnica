from fastapi import APIRouter, Depends,  status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.schemas.users_schemas import AccessTokenOut, ValidateLogin
from src.app.modules.user_module.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login", response_model=AccessTokenOut, status_code=status.HTTP_200_OK)
async def login(
    data: ValidateLogin, db: AsyncSession = Depends(get_db)
) -> AccessTokenOut:
    service = UserService(db)
    return await service.login(data.model_dump())
