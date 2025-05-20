from modules.PermissionModule.models.m_actions import MAction
from services.base_services import BaseService
from modules.PermissionModule.repositories.action_repository import ActionRepository
from modules.PermissionModule.schemas.action_schema import (
    MActionCreateValidator,
    MActionUpdateValidator
)
class ActionService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = ActionRepository(db)
        super().__init__(MAction, self.repo, MActionCreateValidator, MActionUpdateValidator)
