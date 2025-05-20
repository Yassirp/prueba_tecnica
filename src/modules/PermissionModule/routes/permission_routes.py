from flask import Blueprint
from modules.PermissionModule.controllers.permission_controller import PermissionController

permission_bp = Blueprint('permission', __name__)

permission_bp.get('/permissions')(PermissionController.get_all_permissions)
# permission_bp.get('/permissions-with-relationship')(PermissionController.get_all_permissions_with_relationships)
permission_bp.post('/create-permission-with-actions')(PermissionController.create_permission_with_actions)
permission_bp.get('/permission/<int:permission_id>')(PermissionController.get_permission_by_id)
permission_bp.post('/create-permission')(PermissionController.create_permission)
permission_bp.put('/update-permission/<int:permission_id>')(PermissionController.update_permission)
permission_bp.delete('/delete-permission/<int:permission_id>')(PermissionController.delete_permission)
permission_bp.post('/update-permission-by-associate')(PermissionController.update_permission_by_associate)
