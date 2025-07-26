from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser
from src.app.modules.living_group_module.repositories.living_group_users_repository import LivingGroupUserRepository
from src.app.modules.living_group_module.schemas.living_group_user_schemas import LivingGroupUserOut, LivingGroupUserCreate, LivingGroupUserUpdate
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from fastapi import HTTPException, status
from src.app.modules.user_module.models.users import User  
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from src.app.modules.parameters_module.repositories.parameter_values_repository import ParameterValueRepository

class LivingGroupUserService(BaseService[LivingGroupUser, LivingGroupUserOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(
            model=LivingGroupUser,
            repository_cls=LivingGroupUserRepository,
            db_session=db_session,
            out_schema=LivingGroupUserOut,
        )

    async def create(self, data: LivingGroupUserCreate):
        await self._validate_foreign_keys(data)
        return await super().create(data.model_dump())
    
    async def update(self, id: int, data: LivingGroupUserUpdate):
        await self._validate_foreign_keys(data)
        return await super().update(id, data.model_dump())
    
    
    async def _validate_foreign_keys(self, data: LivingGroupUserCreate | LivingGroupUserUpdate):
        if data.living_group_id:
            living_group_repository = LivingGroupRepository(model=LivingGroup, db_session=self.db_session)
            living_group = await living_group_repository.get_by_id(data.living_group_id)
            if not living_group:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Living group no encontrado")
         
        if data.user_id:
            user_repository = UserRepository(model=User, db_session=self.db_session)
            user = await user_repository.get_by_id(data.user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")

        if data.type_id:
            parameter_value_repository = ParameterValueRepository(model=ParameterValue, db_session=self.db_session)
            parameter_value = await parameter_value_repository.get_by_id(data.type_id)
            if not parameter_value:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de usuario no encontrado")
            
        if data.living_group_id:
            living_group_repository = LivingGroupRepository(model=LivingGroup, db_session=self.db_session)
            living_group = await living_group_repository.get_by_id(data.living_group_id)  
            if not living_group:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Living group no encontrado")
    
    async def get_group_and_leader_info(self, living_group_id: int, type_id: int = 4):
        """
        Obtiene información del grupo de vida y líder para un grupo específico
        """
        repository = LivingGroupUserRepository(LivingGroupUser, self.db_session)
        return await repository.get_group_and_leader_info(living_group_id, type_id)
