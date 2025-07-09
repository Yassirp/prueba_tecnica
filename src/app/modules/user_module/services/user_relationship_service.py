from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.user_module.models.user_relationship import UserRelationship
from src.app.modules.user_module.repositories.user_relationship_repository import UserRelationshipRepository
from src.app.modules.user_module.schemas.users_relationship_schemas import UserRelationshipOut 


class UserRelationshipService(BaseService[UserRelationship, UserRelationshipOut]):
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRelationshipRepository(UserRelationship, db_session)
        super().__init__(
            model=UserRelationship,
            repository_cls=UserRelationshipRepository,
            db_session=db_session,
            out_schema=UserRelationshipOut,
        )
        