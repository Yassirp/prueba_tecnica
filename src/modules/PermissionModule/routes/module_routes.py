from flask import Blueprint
from modules.PermissionModule.controllers.module_controller import ModuleController

module_bp = Blueprint('module', __name__)

module_bp.get('/modules')(ModuleController.get_all_modules)
module_bp.get('/module/<int:module_id>')(ModuleController.get_module_by_id)
module_bp.get('/modules-with-relationship')(ModuleController.get_all_with_relationships)
module_bp.post('/create-module')(ModuleController.create_module)
module_bp.put('/update-module/<int:module_id>')(ModuleController.update_module)
module_bp.delete('/delete-module/<int:module_id>')(ModuleController.delete_module)
