from modules.PermissionModule.models.c_permissions import CPermission
from repositories.base_repository import BaseRepository
class PermissionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, CPermission)
        
        
    def permission_exists(self, associate_id, associate_to):
        return self.db.query(self.model).filter(
            self.model.associate_id == associate_id,
            self.model.associate_to == associate_to,
        ).all()