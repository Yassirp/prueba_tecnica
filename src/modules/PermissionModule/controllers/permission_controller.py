from flask import request, jsonify
from database.database import get_db
from modules.PermissionModule.services.permission_services import PermissionService
from utils.serialize import serialize_model
from middleware.auth import require_auth
from utils.permission import require_permission
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
class PermissionController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_all_permissions():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = PermissionService(db)
                permissions,total = service.get_all(limit, offset, order_by, filters)
                
                return jsonify(paginated_response(permissions, total, limit, offset, serialize_model)), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_permission_by_id(permission_id):
        try:
            with get_db() as db:
                service = PermissionService(db)
                permission = service.get_by_id(permission_id)
                if permission:
                    return jsonify(serialize_model(permission)), 200
                return jsonify({'error': 'Permission not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    
    @staticmethod
    @require_auth
    @require_permission("Crear", "Permisos")
    def create_permission():
        try:
            with get_db() as db:
                service = PermissionService(db)
                data = request.json
                permission = service.create(data)
                return jsonify(serialize_model(permission)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Actualizar", "Permisos")
    def update_permission(permission_id):
        try:
            with get_db() as db:
                service = PermissionService(db)
                data = request.json
                permission = service.update(permission_id, data)
                if permission:
                    return jsonify(serialize_model(permission)), 200
                return jsonify({'error': 'Permission not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Permisos")
    def delete_permission(permission_id):
        try:
            with get_db() as db:
                service = PermissionService(db)
                if service.delete(permission_id):
                    return jsonify({'message': 'Permission deleted'}), 200
                return jsonify({'error': 'Permission not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Crear", "Permisos")
    def create_permission_with_actions():
        try:
            with get_db() as db:
                service = PermissionService(db)
                data = request.json
                permission = service.create_permission_with_actions(data, data.module_action_ids)
                return jsonify(permission), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    
    @staticmethod
    @require_auth
    @require_permission("Actualizar", "Permisos")
    def update_permission_by_associate():
        try:
            with get_db() as db:
                service = PermissionService(db)
                data = request.json
                permission = service.update_permissions(data)
                if permission:
                    return jsonify(permission), 200
                return jsonify({'error': 'Permission not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    