from modules.FlowModule.models.m_object_states import MObjectState
from repositories.base_repository import BaseRepository


class ObjectStateRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MObjectState)

