from flask import request, jsonify
from modules.CategoryModule.services.subcategory_detail_services import SubcategoryDetailService
from database.database import get_db
from utils.serialize import serialize_model
from utils.permission import require_permission
from database.redis import redis_client
from utils.request_utils import get_pagination_params, get_filter_params,paginated_response
from middleware.auth import require_auth
class SubcategoryDetailController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_all():
        try:
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            with get_db() as db:
                service = SubcategoryDetailService(db)
                result, total = service.get_all(limit=limit, offset=offset, order_by=order_by,filters=filters)

                return jsonify(paginated_response(result, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_by_id(id):
        try:
            with get_db() as db:
                service = SubcategoryDetailService(db)
                result = service.get_by_id(id)
                if result:
                    return jsonify(serialize_model(result)), 200
                return jsonify({'error': 'Not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    @staticmethod
    @require_auth
    @require_permission("Crear", "Inventario")
    def create():
        try:
            data = request.json
            # user_name = request.user.get('name', 'Usuario desconocido')
            with get_db() as db:
                service = SubcategoryDetailService(db)
                result = service.create(data)
                return jsonify(serialize_model(result)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Actualizar", "Inventario")
    def update(subcategory_detail_id):
        try:
            data = request.json
            # user_name = request.user.get('name', 'Usuario desconocido')
            with get_db() as db:
                service = SubcategoryDetailService(db)
                result = service.update(subcategory_detail_id, data)
                if result:
                    return jsonify(serialize_model(result)), 200
                return jsonify({'error': 'Not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    
    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Inventario")    
    def delete(subcategory_detail_id):
        try:
            with get_db() as db:
                service = SubcategoryDetailService(db)
                if service.delete(subcategory_detail_id):
                    return jsonify({'message': 'Deleted successfully'}), 200
                return jsonify({'error': 'Not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
