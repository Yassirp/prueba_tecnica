from flask import jsonify, request
from modules.CategoryModule.services.region_services import RegionService
from database.database import get_db
from traits.region import DataRegion
from utils.request_utils import get_pagination_params, get_filter_params, paginated_response
from utils.serialize import serialize_model
from middleware.auth import require_auth
from utils.permission import require_permission

class RegionController:
    @staticmethod
    def get_all():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = RegionService(db)
                
                regions, total = service.get_all(limit, offset, order_by, filters) 
                return jsonify(paginated_response(regions, total, limit, offset, serialize_model)), 200

        except Exception as e:
            print(">>> Error:", e)
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_one(region_id):
        try:
            with get_db() as db:
                service = RegionService(db)
                region = service.get_by_id(region_id)
                if not region:
                    return jsonify({"error": "Region not found"}), 404
                return jsonify(DataRegion.from_model(region)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.json
            with get_db() as db:
                service = RegionService(db)
                region = service.create(data)
                return jsonify(DataRegion.from_model(region)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(region_id):
        try:
            data = request.json
            with get_db() as db:
                service = RegionService(db)
                region = service.update(region_id, data)
                if not region:
                    return jsonify({"error": "Region not found"}), 404
                return jsonify(DataRegion.from_model(region)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(region_id):
        try:
            with get_db() as db:
                service = RegionService(db)
                region = service.delete(region_id)
                if not region:
                    return jsonify({"error": "Region not found"}), 404
                return jsonify({"message": "Region deleted"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    def get_all_with_relationship():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = RegionService(db)
                regions, total = service.get_all_with_relationships(limit, offset, order_by, filters) 
                return jsonify(paginated_response(regions, total, limit, offset)), 200

        except Exception as e:
            print(">>> Error:", e)
            return jsonify({'error': str(e)}), 500
        
        

