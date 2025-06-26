from datetime import datetime
from modules.PermissionModule.models.m_module import MModule
from modules.PermissionModule.repositories.module_repository import ModuleRepository
from services.base_services import BaseService
from modules.PermissionModule.schemas.module_schema import (
    MModuleCreate,
    MModuleUpdate
)

class ModuleService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = ModuleRepository(db)
        super().__init__(MModule, self.repo,MModuleCreate, MModuleUpdate)
