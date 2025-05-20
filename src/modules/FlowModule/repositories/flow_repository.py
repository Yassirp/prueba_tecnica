from modules.FlowModule.models.m_flows import MFlow
from repositories.base_repository import BaseRepository


class FlowRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MFlow)

