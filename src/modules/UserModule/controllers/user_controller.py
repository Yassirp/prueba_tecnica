from flask import  jsonify, request, abort
from modules.UserModule.services.user_services import UserService
from utils.permission import require_permission
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params, http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from middleware.auth import require_auth
from database.database import get_db_mysql


class UserController:
    
    @staticmethod
    @require_auth
    def get_all_users():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params() 
            with get_db_mysql() as db:
                service = UserService(db)
                actions, total  = service.get_all(limit, offset, order_by, filters)
                
                return jsonify(paginated_response(actions, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500   
        
    @staticmethod
    def get_user_by_id(user_id):
        with get_db_mysql() as db:
            service = UserService(db)
            action = service.get_by_id(user_id)
            if action:
                return jsonify(serialize_model(action)), 200
            return jsonify({'error': 'User not found'}), 404
        

    @staticmethod
    def create_user():
        with get_db_mysql() as db:
            service = UserService(db)
            try:
                data = request.json
                action = service.create(data)
                return jsonify(serialize_model(action)), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500


    @staticmethod
    def update_user(user_id):
        with get_db_mysql() as db:
            service = UserService(db)
            try:
                data = request.json
                action = service.update(user_id, data)
                if action:
                    return jsonify(serialize_model(action)), 200
                return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500


    @staticmethod
    def delete_user(user_id):
        with get_db_mysql() as db:
            service = UserService(db)
            if service.delete(user_id):
                return jsonify({'message': 'User deleted'}), 200
            return jsonify({'error': 'User not found'}), 404
