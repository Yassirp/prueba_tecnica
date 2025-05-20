from modules.PermissionModule.models.m_role import MRole
from modules.PermissionModule.repositories.role_repository import RoleRepository
from services.base_services import BaseService
from modules.PermissionModule.schemas.role_schema import MRoleCreate, MRoleUpdate
class RoleService(BaseService):
    def __init__(self, db):
        self.repository = RoleRepository(db)
        super().__init__(MRole, self.repository,MRoleCreate, MRoleUpdate)
