# Archivo generado automáticamente para access_tokens - services
import hashlib
import secrets
import pytz
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

class AccessTokenService(BaseService[AccessToken, AccessTokenOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=AccessToken,
            repository_cls=AccessTokenRepository,
            db_session=db_session,
            out_schema=AccessTokenOut,
        )
        self.db_session = db_session  # << ¡Esto es lo que falta!
        self.project_service = ProjectService(db_session)

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).where(self.model.state == Setting.STATUS.value)

            conditions = []
            if token:
                conditions.append(self.model.token == token)

            # Aplicar condiciones al query
            if conditions:
                stmt = stmt.where(and_(*conditions))

            # Ordenamiento
            if order_by:
                stmt = stmt.order_by(order_by)

            # Paginación
            if offset:
                stmt = stmt.offset(offset)
                
            if limit:
                stmt = stmt.limit(limit)

            # Ejecutar query
            result = await self.db_session.execute(stmt)
            items = result.scalars().all()
            total = len(items)

            return items, total
        except Exception as e:
            raise e
        

    async def login(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            key = data.get("key")
            project_id = data.get("project_id")
            user_id= data.get("user_id", None)
            hashed_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
            # Validamos si existe el proyecto
            project = await self.project_service.get_by_id(project_id)
            
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'.",
            )

            if project["key"] != hashed_key:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se ha encontrado una empresa asociada a esta clave.",
            )

            # Crear objeto AccessToken
            access_token = AccessToken(
                token=secrets.token_hex(32),
                project_id=project["id"],
                user_id=user_id if user_id else None,
                expires_at=datetime.now(pytz.timezone("America/Bogota")) + timedelta(hours=24),
                created_at=datetime.now(pytz.timezone("America/Bogota")),
            )

            # Guardar en DB
            self.db_session.add(access_token)
            await self.db_session.commit()
 
            return [access_token.token]
        except Exception as e:
            raise e
        

    async def logout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            token = data.get("token", None)
            
            model, count = await self.get_all(token=token)
            if not count:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"el token {token} no existe.",
            )
            for value in model:
                await self.db_session.delete(value)

            await self.db_session.commit()

            return []
        except Exception as e:
            raise e 