from flask import request, jsonify
from database.database import get_db
from modules.ParameterModule.services.pv_services import ParameterValueService
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
class PVController:

    @staticmethod
    def get_all_parameter_values():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = ParameterValueService(db)
                values, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filters)
                return jsonify(paginated_response(values, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_parameter_value_by_id(id):
        try:
            with get_db() as db:
                service = ParameterValueService(db)
                value = service.get_by_id(id)
                if value:
                    return jsonify(serialize_model(value)), 200
                return jsonify({'error': 'Parameter value not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create_parameter_value():
        try:
            with get_db() as db:
                service = ParameterValueService(db)
                data = request.json
                value = service.create(data)
                return jsonify(serialize_model(value)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_parameter_value(pv_id):
        try:
            with get_db() as db:
                service = ParameterValueService(db)
                data = request.json
                value = service.update(pv_id, data)
                if value:
                    return jsonify(serialize_model(value)), 200
                return jsonify({'error': 'Parameter value not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete_parameter_value(pv_id):
        try:
            with get_db() as db:
                service = ParameterValueService(db)
                if service.delete(pv_id):
                    return jsonify({'message': 'Parameter value deleted'}), 200
                return jsonify({'error': 'Parameter value not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_all_parameter_values_by_parameter_reference():
        try:
            data = request.json
            with get_db() as db:
                service = ParameterValueService(db)
                values = service.get_parameter_value_by_parameter_reference(data.get("reference"))
                return jsonify(values), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500