# Archivo generado automáticamente para access_tokens - routes

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from src.app.config.database.session import get_db
from src.app.modules.access_tokens_module.schemas.access_tokens_schemas import (
    AccessTokenOut,
    ValidateLogin
    )

from src.app.modules.access_tokens_module.services.access_tokens_service import AccessTokenService
from src.app.modules.document_rules_module.services.document_rules_service import DocumentRuleService
from src.app.shared.constants.messages import LoginMessages
from src.app.shared.utils.request_utils import paginated_response
from src.app.decorators.route_responses import handle_route_responses


router = APIRouter(prefix="/auth", tags=["Auth"])

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
