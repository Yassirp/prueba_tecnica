from flask import Blueprint
from modules.PermissionModule.controllers.module_action_controller import ModuleActionController

module_action_bp = Blueprint('module_action', __name__)

module_action_bp.get('/module-actions')(ModuleActionController.get_all_module_actions)
module_action_bp.get('/module-action/<int:module_action_id>')(ModuleActionController.get_module_action_by_id)
module_action_bp.post('/create-module-action')(ModuleActionController.create_module_action)
module_action_bp.post('/create-module-actions')(ModuleActionController.create_module_actions)
module_action_bp.put('/update-module-action/<int:module_action_id>')(ModuleActionController.update_module_action)
module_action_bp.delete('/delete-module-action/<int:module_action_id>')(ModuleActionController.delete_module_action)
module_action_bp.post('/sync-and-attach-module-action')(ModuleActionController.sync_and_attach_module_action)