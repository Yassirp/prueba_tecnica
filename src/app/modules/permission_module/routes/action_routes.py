from flask import Blueprint
from modules.PermissionModule.controllers.action_controller import ActionController

action_bp = Blueprint('actions', __name__)

action_bp.route('/actions', methods=['GET'])(ActionController.get_all_actions)
action_bp.route('/action/<int:action_id>', methods=['GET'])(ActionController.get_action_by_id)
action_bp.route('/create-action', methods=['POST'])(ActionController.create_action)
action_bp.route('/update-action/<int:action_id>', methods=['PUT'])(ActionController.update_action)
action_bp.route('/delete-action/<int:action_id>', methods=['DELETE'])(ActionController.delete_action)
