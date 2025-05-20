from modules.PermissionModule.models.c_permissions import CPermission
from modules.PermissionModule.repositories.permission_repository import PermissionRepository
from services.base_services import BaseService
from modules.PermissionModule.schemas.permission_schema import (
    CPermissionCreate, CPermissionUpdate)
from utils.serialize import serialize_model
class PermissionService(BaseService):
    def __init__(self, db):
        self.repo = PermissionRepository(db)
        super().__init__(CPermission, self.repo, CPermissionCreate, CPermissionUpdate)
        
        
    def create_permission_with_actions(self, data, action_ids):
        try:
            data_response= []
            for action_id in action_ids:
                module_action = self.create({
                    'associate_id': data['associate_id'],
                    'associate_to': data['associate_to'],
                    'action_id': action_id
                })
                data_response.append(serialize_model(module_action))
            
            return data_response    
        except Exception as e:
            raise e
        
    
    def update_permissions(self, data):
        try:
            self.remove_existing_permissions(data['associate_id'], data['associate_to'])
                
            data_label= {
                "associate_id": data['associate_id'],
                "associate_to": data['associate_to']
            }
            permission_create = self.create_permission_with_actions(data_label, data['module_actions'])
            return permission_create    
        except Exception as e:
            raise e
        
        
    def remove_existing_permissions(self, associate_id, associate_to):
        permissions = self.repo.permission_exists(associate_id, associate_to)
        for p in permissions:
            self.repo.delete(p.id)
            