from flask import request, jsonify
from database.database import get_db
from modules.ParameterModule.services.parameter_services import ParameterService
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
class ParameterController:

    @staticmethod
    def get_all_parameters():
        try:
            limit, offset, order_by = get_pagination_params()
            filters = get_filter_params()
            with get_db() as db:
                service = ParameterService(db)
                parameters, total = service.get_all(limit, offset, order_by, filters)
                
                return jsonify(paginated_response(parameters, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_parameter_by_id(parameter_id):
        try:
            with get_db() as db:
                service = ParameterService(db)
                parameter = service.get_by_id(parameter_id)
                if parameter:
                    return jsonify(serialize_model(parameter)), 200
                return jsonify({'error': 'Parameter not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create_parameter():
        try:
            with get_db() as db:
                service = ParameterService(db)
                data = request.json
                parameter = service.create(data)
                return jsonify(serialize_model(parameter)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_parameter(parameter_id):
        try:
            with get_db() as db:
                service = ParameterService(db)
                data = request.json
                parameter = service.update(parameter_id, data)
                if parameter:
                    return jsonify(serialize_model(parameter)), 200
                return jsonify({'error': 'Parameter not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete_parameter(parameter_id):
        try:
            with get_db() as db:
                service = ParameterService(db)
                if service.delete(parameter_id):
                    return jsonify({'message': 'Parameter deleted'}), 200
                return jsonify({'error': 'Parameter not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
