from flask import request, jsonify
from database.database import get_db
from modules.CategoryModule.services.product_services import ProductService
from utils.serialize import serialize_model
from utils.permission import require_permission
from utils.request_utils import get_pagination_params, paginated_response,http_response,get_filter_params
from utils.global_message import GlobalMessages
from http import HTTPStatus
from middleware.auth import require_auth
class ProductController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_all_products():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = ProductService(db)
                products, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filter)

                return jsonify(paginated_response(products, total, limit, offset, serialize_model)), 200

        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)


    
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    
    def get_product_by_id(id):
        try:
            with get_db() as db:
                service = ProductService(db)
                product = service.get_by_id(id)
                if product:
                    return jsonify(serialize_model(product)), 200
                return jsonify({'error': 'Product not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    
    def create_product():
        try:
            with get_db() as db:
                service = ProductService(db)
                data = request.json
                product = service.create(data)
                return jsonify(serialize_model(product)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    
    def update_product(id):
        try:
            with get_db() as db:
                service = ProductService(db)
                data = request.json
                product = service.update(id, data)
                if product:
                    return jsonify(serialize_model(product)), 200
                return jsonify({'error': 'Product not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def delete_product(id):
        try:
            with get_db() as db:
                service = ProductService(db)
                if service.delete(id):
                    return jsonify({'message': 'Product deleted'}), 200
                return jsonify({'error': 'Product not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Inventario")
    def get_all_products_with_relationship():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = ProductService(db)
                products, total = service.get_all_with_relationships(limit=limit, offset=offset, order_by=order_by, filters=filter)

                return jsonify(paginated_response(products, total, limit, offset)), 200

        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)