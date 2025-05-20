from modules.PermissionModule.models.m_actions import MAction
from repositories.base_repository import BaseRepository

class ActionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MAction)

