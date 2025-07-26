from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.modules.user_module.models.users import User

class LivingGroupUserRepository(BaseRepository[LivingGroupUser]):
    def __init__(self, model: type[LivingGroupUser], db_session: AsyncSession):
        super().__init__(model, db_session)
    
    async def get_group_and_leader_info(self, user_id: int, type_id: int = 4):
        """
        Obtiene información del grupo de vida y líder para un usuario específico
        basado en la consulta SQL proporcionada
        """
        query = select(
            LivingGroup.name,
            LivingGroup.description,
            User.name,
            User.last_name
        ).select_from(
            join(
                LivingGroupUser,
                LivingGroup,
                LivingGroupUser.living_group_id == LivingGroup.id
            ).join(
                User,
                LivingGroupUser.user_id == User.id
            )
        ).where(
            LivingGroupUser.user_id == user_id,
            LivingGroupUser.type_id == type_id
        )
        
        result = await self.db_session.execute(query)
        return result.fetchone()
