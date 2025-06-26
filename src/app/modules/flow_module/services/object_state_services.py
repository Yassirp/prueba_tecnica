from modules.FlowModule.models.m_object_states import MObjectState
from modules.FlowModule.repositories.object_state_repository import ObjectStateRepository
from modules.FlowModule.schemas.object_state_schema import ObjectStateCreate, ObjectStateUpdate
from services.base_services import BaseService


class ObjectStateService(BaseService):

    def __init__(self, db):
        self.db = db
        self.repo = ObjectStateRepository(db)
        super().__init__(
            MObjectState,
            self.repo,
            ObjectStateCreate,
            ObjectStateUpdate
        )

