from modules.PermissionModule.models.c_module_actions import CModuleAction
from modules.PermissionModule.repositories.module_action_repository import ModuleActionRepository
from services.base_services import BaseService
from utils.serialize import serialize_model
from modules.PermissionModule.schemas.module_action_schema import (
    CModuleActionCreate, CModuleActionUpdate)

class ModuleActionService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = ModuleActionRepository(db)
        super().__init__(CModuleAction, self.repo,CModuleActionCreate, CModuleActionUpdate)


    def create_with_actions(self, module_id, action_ids):

        try:
            data= []
            for action_id in action_ids:
                module_action = self.create({
                    'module_id': module_id,
                    'action_id': action_id
                })
                data.append(serialize_model(module_action))
            
            return data    
        except Exception as e:
            raise e
        
        
    def  sync_and_attach_module_action(self,data):
        try:
            
            module_id = data['module_id']
            self.remove_existing_module_actions(module_id)
            
            return self.create_with_actions(module_id, data['action_ids'])   
        except Exception as e:
            raise e
        
        
    def remove_existing_module_actions(self, module_id):
        try:
            modules, _m= self.get_all(filters={'module_id': module_id})
            print(modules)
            for m in modules:
                self.repo.delete(m.id)
       
            return True     
        except Exception as e:
            raise e
        
        