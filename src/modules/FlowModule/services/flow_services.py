from modules.FlowModule.models.m_flows import MFlow
from modules.FlowModule.repositories.flow_repository import FlowRepository
from modules.FlowModule.schemas.flow_schema import FlowCreate, FlowUpdate
from services.base_services import BaseService


class FlowService(BaseService):

    def __init__(self, db):
        self.db = db
        self.repo = FlowRepository(db)
        super().__init__(
            MFlow,
            self.repo,
            FlowCreate,
            FlowUpdate
        )
