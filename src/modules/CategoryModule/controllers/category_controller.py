from flask import request, jsonify
from modules.CategoryModule.services.category_services import CategoryService
from database.database import get_db
from utils.serialize import serialize_model
from utils.permission import require_permission
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
from middleware.auth import require_auth
class CategoryController:
    
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_all():
        with get_db() as db:
            service = CategoryService(db)
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            categories, total = service.get_all(limit, offset, order_by, filters)
                
            return jsonify(paginated_response(categories, total, limit, offset, serialize_model)), 200

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_by_id(category_id):
        with get_db() as db:
            service = CategoryService(db)
            category = service.get_by_id(category_id)
            if category:
                return jsonify(serialize_model(category))
            return jsonify({'error': 'Category not found'}), 404

    @staticmethod
    @require_auth
    @require_permission("Crear", "Inventario")
    def create():
        try:
            data = request.json
            with get_db() as db:
                service = CategoryService(db)
                category = service.create(data)
                return jsonify(serialize_model(category)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Editar", "Inventario")
    def update(category_id):
        try:
            data = request.json
            with get_db() as db:
                service = CategoryService(db)
                updated = service.update(category_id, data)
                if updated:
                    return jsonify(serialize_model(updated))
                return jsonify({'error': 'Category not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Inventario")
    def delete(category_id):
        with get_db() as db:
            service = CategoryService(db)
            deleted = service.delete(category_id)
            if deleted:
                return jsonify({'message': 'Category deleted'})
            return jsonify({'error': 'Category not found'}), 404


    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Inventario")
    def get_All_with_relationship():
        with get_db() as db:
            service = CategoryService(db)
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            categories, total = service.get_all_with_relationships(limit, offset, order_by, filters)
                
            return jsonify(paginated_response(categories, total, limit, offset)), 200
        
        
    @staticmethod
    @require_auth
    @require_permission("Crear", "Inventario")
    def create_category_with_region():
        with get_db() as db:
            service= CategoryService(db)
            data = request.json
            category_region = service.create_with_region(data)
            
            return category_region
            
            