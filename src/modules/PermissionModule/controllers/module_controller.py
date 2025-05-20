from flask import request, jsonify
from database.database import get_db
from modules.PermissionModule.services.module_services import ModuleService
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
from middleware.auth import require_auth
from utils.permission import require_permission
class ModuleController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_all_modules():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = ModuleService(db)
                modules, total = service.get_all(limit, offset, order_by, filters)
                
                return jsonify(paginated_response(modules, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_module_by_id(module_id):
        try:
            with get_db() as db:
                service = ModuleService(db)
                module = service.get_by_id(module_id)
                if module:
                    return jsonify(serialize_model(module)), 200
                return jsonify({'error': 'Module not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    @staticmethod
    @require_auth
    @require_permission("Crear", "Permisos")
    def create_module():
        try:
            with get_db() as db:
                service = ModuleService(db)
                data = request.json
                module = service.create(data)
                return jsonify(serialize_model(module)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Actualizar", "Permisos")
    def update_module(module_id):
        try:
            with get_db() as db:
                service = ModuleService(db)
                data = request.json
                module = service.update(module_id, data)
                if module:
                    return jsonify(serialize_model(module)), 200
                return jsonify({'error': 'Module not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Permisos")
    def delete_module(module_id):
        try:
            with get_db() as db:
                service = ModuleService(db)
                if service.delete(module_id):
                    return jsonify({'message': 'Module deleted'}), 200
                return jsonify({'error': 'Module not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_all_with_relationships():
        limit, offset, order_by = get_pagination_params()
        filters = get_filter_params() 
        with get_db() as db:
            service = ModuleService(db)
            roles, total = service.get_all_with_relationships(limit, offset, order_by, filters)
            return jsonify({
                "total": total,
                "limit": limit,
                "offset": offset,
                "items": roles
            }), 200