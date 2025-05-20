from flask import  jsonify, request, abort
from modules.FlowModule.services.flow_object_state_services import FlowObjectStateService
from utils.permission import require_permission
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params
from middleware.auth import require_auth
from database.database import get_db
from utils.request_utils import http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from pydantic import ValidationError

class FlowObjectStateController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Flujo de estados")
    def get_flows():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = FlowObjectStateService(db)
                flow, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters=filter)
            
                return jsonify(paginated_response(flow, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Flujo de estados")
    def get_flow(flow_object_state_id: int):
        try:
            with get_db() as db:
                service = FlowObjectStateService(db)
                flow = service.get_by_id(flow_object_state_id)
                if not flow:
                    abort(404, description="flow not found")
                return jsonify(serialize_model(flow))
        except Exception as e:
            abort(500, description=f"Error retrieving flow: {str(e)}")


    @require_auth
    @staticmethod
    @require_permission("Crear", "Flujo de estados")
    def create_flow():
        data = request.get_json()
        with get_db() as db:
            service = FlowObjectStateService(db)
            try:
                action = service.create(data)
                return jsonify(serialize_model(action))
            except ValidationError as e:
                return jsonify({
                    "message": "Error de validación",
                    "errors": e.errors()
                }), HTTPStatus.BAD_REQUEST
            except Exception as e:
                return jsonify({
                    "message": GlobalMessages.ERROR_CREATED,
                    "detail": str(e)
                }), HTTPStatus.INTERNAL_SERVER_ERROR

    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Flujo de estados")
    def update_flow(flow_object_state_id: int):
        data = request.get_json()
        with get_db() as db:
            service = FlowObjectStateService(db)
            try:
                action = service.update(flow_object_state_id, data)
                return jsonify(serialize_model(action))
            except ValidationError as e:
                return jsonify({
                    "message": "Error de validación",
                    "errors": e.errors()
                }), HTTPStatus.BAD_REQUEST
            except Exception as e:
                return jsonify({
                    "message": GlobalMessages.ERROR_UPDATED,
                    "detail": str(e)
                }), HTTPStatus.INTERNAL_SERVER_ERROR


    @require_auth
    @staticmethod
    @require_permission("Eliminar", "Flujo de estados")
    def delete_flow( flow_object_state_id: int):
        try:
            with get_db() as db:
                service = FlowObjectStateService(db)
                flow = service.delete(flow_object_state_id)
                if not flow:
                    abort(404, description="flow not found")
                return jsonify({"message": "flow deleted"})
        except Exception as e:
            abort(500, description=f"Error deleting flow: {str(e)}")
