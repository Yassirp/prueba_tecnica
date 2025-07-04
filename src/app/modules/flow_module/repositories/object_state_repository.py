from src.app.modules.flow_module.models.object_states import ObjectState
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ObjectStateRepository(BaseRepository[ObjectState]):
    def __init__(self, model: type[ObjectState], db_session: AsyncSession):
        super().__init__(model, db_session)
