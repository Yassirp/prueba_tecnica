from flask import request, jsonify
from modules.PermissionModule.services.action_services import ActionService
from middleware.auth import require_auth
from utils.permission import require_permission
from database.database import get_db
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response,get_filter_params
class ActionController:
    # @require_auth
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_all_actions():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params() 
            with get_db() as db:
                service = ActionService(db)
                actions, total  = service.get_all(limit, offset, order_by, filters)
                
                return jsonify(paginated_response(actions, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500   
        
    @staticmethod    
    @require_auth
    @require_permission("Acceder", "Permisos")
    def get_action_by_id(action_id):
        with get_db() as db:
            service = ActionService(db)
            action = service.get_by_id(action_id)
            if action:
                return jsonify(serialize_model(action)), 200
            return jsonify({'error': 'Action not found'}), 404
        

    @staticmethod
    @require_auth
    @require_permission("Crear", "Permisos")
    def create_action():
        with get_db() as db:
            service = ActionService(db)
            try:
                data = request.json
                action = service.create(data)
                return jsonify(serialize_model(action)), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Actualizar", "Permisos")
    def update_action(action_id):
        with get_db() as db:
            service = ActionService(db)
            try:
                data = request.json
                action = service.update(action_id, data)
                if action:
                    return jsonify(serialize_model(action)), 200
                return jsonify({'error': 'Action not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500



    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Permisos")
    def delete_action(action_id):
        with get_db() as db:
            service = ActionService(db)
            if service.delete(action_id):
                return jsonify({'message': 'Action deleted'}), 200
            return jsonify({'error': 'Action not found'}), 404
