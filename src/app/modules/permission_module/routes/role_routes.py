from flask import Blueprint
from modules.PermissionModule.controllers.role_controller import RoleController

role_bp = Blueprint('role', __name__)

role_bp.route('/roles', methods=['GET'])(RoleController.get_all)
role_bp.route('/rol/<int:role_id>', methods=['GET'])(RoleController.get_by_id)
role_bp.route('/create-rol', methods=['POST'])(RoleController.create)
role_bp.route('/update-rol/<int:role_id>', methods=['PUT'])(RoleController.update)
role_bp.route('/delete-rol/<int:role_id>', methods=['DELETE'])(RoleController.delete)
role_bp.get('/roles-with-relationship')(RoleController.get_all_with_relationships)