from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.user_module.controllers.user_controller import UserController
from src.app.shared.constants.messages import (
    LoginMessages, 
    LogoutMessages
    )

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login", response_model=AccessTokenOut, status_code=status.HTTP_201_CREATED)
@handle_route_responses(
    success_message=LoginMessages.SUCCESS,
    error_message=LoginMessages.ERROR,
)
async def create_document_rule(
    data: ValidateLogin, db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    try:    
        service = AccessTokenService(db)
        return await service.login(data.model_dump())
    except Exception as e:
        raise e
