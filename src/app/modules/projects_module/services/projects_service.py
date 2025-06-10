import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from io import BytesIO
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.app.shared.bases.base_service import BaseService
from src.app.modules.projects_module.models.projects import Project
from src.app.modules.projects_module.repositories.projects_repository import (
    ProjectRepository,
)
from src.app.modules.projects_module.schemas.projects_schemas import ProjectOut

class ProjectService(BaseService[Project, ProjectOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Project,
            repository_cls=ProjectRepository,
            db_session=db_session,
            out_schema=ProjectOut,
        )

        self.db_session = db_session

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model)
            
            # FIltramos por key
            if key:
                stmt = stmt.where(self.model.key == str(key))

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


    async def create_key(self, data, encode=True):
        try:
            key = data.get('key', None)
            if not key:
                raise ValueError("La clave 'key' es obligatoria")
    
            # Utiliza la contraseña proporcionada como sal
            salt = key.encode()
    
            # Deriva la clave utilizando PBKDF2HMAC
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            derived_key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
            fernet = Fernet(derived_key)
    
            if encode:
                encrypted_key = fernet.encrypt(key.encode())
                # Codifica el valor en base64 y conviértelo a una cadena de texto
                encrypted_key_str = base64.urlsafe_b64encode(encrypted_key).decode()
                return encrypted_key_str
            else:
                # Decodifica el valor de base64 y desencripta
                encrypted_key = base64.urlsafe_b64decode(key.encode())
                decrypted_key = fernet.decrypt(encrypted_key).decode()
                return decrypted_key
        except Exception as e:
            raise e


    async def _validate_data(self, data):
        try:
            key = data.get('key',None)
            name = data.get('name',None)
            value = await self.create_key(data)
            project, count  = await self.get_all(key=key)
            if count:
                for model in project:
                    if model.name == name:
                        print("model.name: ",model.name)
                        print("model.name: ",name)
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"El nombre '{name}' ya se encuentra registrado.",
                        )
                    #value = await self.create_key(data)
                    if model.key == key:
                       raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"la key '{key}' ya se encuentra registrada.",
                        )
            return True
        except Exception as e:
            raise e

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            await self._validate_data(data)
            #nre_key = await self.create_key(data)
            #data['key'] = nre_key
            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e