from flask import request, jsonify
from modules.CategoryModule.services.category_region_services import CategoryRegionService
from database.database import get_db
from utils.serialize import serialize_model
from utils.permission import require_permission
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
from middleware.auth import require_auth

class CategoryRegionController:
    
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_all():
        with get_db() as db:
            service = CategoryRegionService(db)
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            categories, total = service.get_all(limit, offset, order_by, filters)
                
            return jsonify(paginated_response(categories, total, limit, offset, serialize_model)), 200

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_by_id(category_id):
        with get_db() as db:
            service = CategoryRegionService(db)
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
                service = CategoryRegionService(db)
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
                service = CategoryRegionService(db)
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
            service = CategoryRegionService(db)
            deleted = service.delete(category_id)
            if deleted:
                return jsonify({'message': 'Category deleted'})
            return jsonify({'error': 'Category not found'}), 404


    @staticmethod
    @require_auth
    @require_permission("Eliminar", "Inventario")
    def get_All_with_relationship():
        with get_db() as db:
            service = CategoryRegionService(db)
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            categories, total = service.get_all_with_relationships(limit, offset, order_by, filters)
                
            return jsonify(paginated_response(categories, total, limit, offset)), 200
    
    
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_subcategories_by_region(region_id):
        try:
            with get_db() as db:
                service = CategoryRegionService(db)
                filters = get_filter_params()
                
                subcategories = service.get_subcategories_by_region(region_id, filters)
                
                if not subcategories:
                    return jsonify({"error": "No se encontraron subcategoría para esta región", 'subcategory': subcategories}), 404

                return jsonify(subcategories), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500