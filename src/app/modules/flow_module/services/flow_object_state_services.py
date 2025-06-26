from modules.FlowModule.models.m_flow_object_states import MFlowObjectState
from modules.FlowModule.repositories.fos_repository import FOSRepository
from modules.FlowModule.schemas.flow_object_state_schema import FlowObjectStateCreate, FlowObjectStateUpdate
from services.base_services import BaseService


class FlowObjectStateService(BaseService):

    def __init__(self, db):
        self.db = db
        self.repo = FOSRepository(db)
        super().__init__(
            MFlowObjectState,
            self.repo,
            FlowObjectStateCreate,
            FlowObjectStateUpdate
        )