from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.user_module.models import user_relationship
from src.app.shared.bases.base_service import BaseService
from src.app.modules.user_module.models.users import User
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.user_module.schemas.users_schemas import UserOut, UserCreate, UserOutWithRelationships
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.parameters_module.repositories.parameter_values_repository import ParameterValueRepository
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from src.app.modules.flow_module.repositories.object_state_repository import ObjectStateRepository
from src.app.modules.flow_module.models.object_states import ObjectState
from src.app.modules.user_module.repositories.user_relationship_repository import UserRelationshipRepository
from src.app.modules.user_module.models.user_relationship import UserRelationship
from src.app.modules.living_group_module.services.living_group_user_service import LivingGroupUserService
from src.app.modules.living_group_module.schemas.living_group_user_schemas import LivingGroupUserCreate
from passlib.context import CryptContext
from fastapi import HTTPException, status
import random
from fastapi.responses import JSONResponse
import string
import asyncio
from src.app.shared.utils.request_utils import http_response
from src.app.shared.utils.service_token import send_email_token, send_sms_token
from src.app.utils.mailer import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserOut]):
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(User, db_session)
        self.user_relationship_repository = UserRelationshipRepository(UserRelationship, db_session)
        self.parameter_value_repository = ParameterValueRepository(model=ParameterValue, db_session=db_session)
        self.object_state_repository = ObjectStateRepository(ObjectState, db_session)
        self.living_group_user_service = LivingGroupUserService(db_session)
        super().__init__(
            model=User,
            repository_cls=UserRepository,
            db_session=db_session,
            out_schema=UserOut,
        )
        
    async def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = {}) -> tuple:
        users, total = await self.repository.get_all_with_relationships(limit, offset, order_by, filters)
        return users, total
    
    
    async def get_by_id_with_relations(self, user_id: int):
        user =  await self.repository.get_by_id_with_relations(user_id) 
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        user_with_relations = await self._assigment_relationship(user)
        return user_with_relations


    async def _assigment_relationship(self, user: User):
        if not user:
            return user

        # Obtener relaciones donde el usuario es el iniciador
        user_relationships = await self.user_relationship_repository.get_by_user_id(getattr(user, 'id'))
        user_relationships_2 = await self.user_relationship_repository.get_by_user_relationship_id(getattr(user, 'id'))
        user_relationships_v2 = []
        if user_relationships:
            for relationship in user_relationships:
                # Asignar las relaciones obtenidas
                relationship.user_relationship = await self.repository.get_basic_by_id(getattr(relationship, 'user_relationship_id'))
                relationship.relationship_status = await self.object_state_repository.get_by_id(relationship.relationship_status_id)
                relationship.relationship_type = await self.parameter_value_repository.get_by_id(relationship.relationship_type_id)
                user_relationships_v2.append(relationship)
                
        if user_relationships_2:
            for relationship in user_relationships_2:
                relationship.user_relationship = await self.repository.get_basic_by_id(getattr(relationship, 'user_id'))
                relationship.relationship_status = await self.object_state_repository.get_by_id(relationship.relationship_status_id)
                relationship.relationship_type = await self.parameter_value_repository.get_by_id(relationship.relationship_type_id)
                user_relationships_v2.append(relationship)
        
        user.user_relationships_v2 = user_relationships_v2
            
        return user
            
        
    async def register(self, data: dict) -> JSONResponse:
        # Validar que el email sea único
        existing_user = await self.repository.get_by_email(data["email"])
        if existing_user:
            return http_response(status=400, message="El email ya está registrado")
        
        # Generar código de 6 dígitos
        code = str(random.randint(100000, 999999))
        data["code"] = code
        data["password"] = pwd_context.hash(data["password"])

        user = UserCreate(**data)
        new_user = await self.repository.create(user.model_dump())
        if data.get("participated_in_living_group"):
            living_group_user_data = LivingGroupUserCreate(
                user_id=getattr(new_user, 'id'),
                living_group_id=data["living_group_id"],
                type_id=data["type_id"] if "type_id" in data else 1,
                description=data["description"] if "description" in data else None,
                data=data["data"] if "data" in data else None,
                active=data["active"] if "active" in data else True
            )
            living_group_user = await self.living_group_user_service.create(living_group_user_data)

        # 3. Enviar la contraseña por correo
        await send_email(
            to_email=data['email'],
            subject="Bienvenido a LVR - Tu cuenta ha sido creada",
            template_name="create-template-user.html",
            context={
                "user_name": f"{data['name']} {data['last_name']}",
                "password": data["password"],
                "leader_name": data["leader_name"],
                "group_name": data["living_group_name"],
                "description": data["description"] if "description" in data else "No hay descripción del grupo pero si un mensaje de ejemplo. Fecha: 30210"
            }
        )

        return http_response(
            message="Usuario registrado correctamente",
            data={"user": new_user}
        )
    

    async def update(self, entity_id: int, data: dict) :
        # Validar que el email sea único si se está actualizando
        if "email" in data:
            existing_user = await self.repository.get_by_email(data["email"])
            if existing_user is not None:
                # Verificar si el usuario encontrado es diferente al que se está actualizando
                existing_id = getattr(existing_user, 'id', None)
                if existing_id is not None and existing_id != entity_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El email ya está registrado por otro usuario"
                    )
        
        # Si se está actualizando la contraseña, hashearla
        if "password" in data:
            data["password"] = pwd_context.hash(data["password"])
        
        updated_user = await self.repository.update(entity_id, data)
        
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
            
    
        return http_response(
            message="Usuario actualizado correctamente",
            data={"user": updated_user}
        )
    
    async def create_user(self, data: dict) -> JSONResponse:
        # 1. Generar contraseña aleatoria
        password_length = 10
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
        
        # 2. Hashear la contraseña y asignarla
        data['password'] = pwd_context.hash(random_password)
        
        if "role_id" not in data:
            data["role_id"] = 2
            
        
        user = UserCreate(**data)
        if "email" in data:
            existing_user = await self.repository.get_by_email(data["email"])
            if existing_user is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado por otro usuario"
                )
            
        new_user = await self.repository.create(user.model_dump())
        if data.get("participated_in_living_group"):
            living_group_user_data = LivingGroupUserCreate(
                user_id=getattr(new_user, 'id'),
                living_group_id=data["living_group_id"],
                type_id=data["type_id"] if "type_id" in data else 1,
                description=data["description"] if "description" in data else None,
                data=data["data"] if "data" in data else None,
                active=data["active"] if "active" in data else True
            )
            await self.living_group_user_service.create(living_group_user_data)

        # 3. Enviar la contraseña por correo
        await send_email(
            to_email=data['email'],
            subject="Bienvenido a LVR - Tu cuenta ha sido creada",
            template_name="create-template-user.html",
            context={
                "user_name": f"{data['name']} {data['last_name']}",
                "password": random_password,
                "leader_name": data["leader_name"],
                "group_name": data["living_group_name"],
                "description": data["description"]
            }
        )
        
        # 4. Retornar respuesta
        return http_response(
            message="Usuario creado correctamente. Se ha enviado la contraseña por correo electrónico.",
            data={"user": new_user}
        )