from modules.FlowModule.models.m_flow_object_states import MFlowObjectState
from repositories.base_repository import BaseRepository


class FOSRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MFlowObjectState)


    def get_order_and_flow(self, order_state, flow_id ):
        return self.db.query(self.model).filter(self.model.order_state == order_state).filter(self.model.flow_id == flow_id).first()