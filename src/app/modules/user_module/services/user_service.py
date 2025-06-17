
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from src.app.modules.projects_module.services.projects_service import ProjectService
from src.app.shared.constants.project_enum import Projectds, Setting
from src.app.modules.access_tokens_module.models.access_tokens import AccessToken
from src.app.modules.access_tokens_module.repositories.access_tokens_repository import AccessTokenRepository
from src.app.modules.access_tokens_module.schemas.access_tokens_schemas import AccessTokenOut
from src.app.shared.bases.base_service import BaseService
load_dotenv()

class UserService(BaseService[User, UserOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=User,
            repository_cls=UserRepository,
            db_session=db_session,
            out_schema=UserOut,
        )
        self.db_session = db_session  # << ¡Esto es lo que falta!
        self.project_service = ProjectService(db_session)
