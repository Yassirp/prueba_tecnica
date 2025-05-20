from modules.PermissionModule.models.c_module_actions import CModuleAction
from repositories.base_repository import BaseRepository

class ModuleActionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, CModuleAction)
