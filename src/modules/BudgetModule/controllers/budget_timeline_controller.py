from flask import  jsonify, request, abort
from modules.BudgetModule.services.budget_timeline_services import BudgetTimelineService
from utils.permission import require_permission
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params, http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from middleware.auth import require_auth
from database.database import get_db


class BudgetTimelineController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def get_all():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = BudgetTimelineService(db)
                budgets, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters= filter)
            
                return jsonify(paginated_response(budgets, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def get(budget_timeline_id: int):
        with get_db() as db:
            try:
                service = BudgetTimelineService(db)
                budget = service.get_by_id(budget_timeline_id)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(serialize_model(budget))
            except Exception as e:
                return http_response(GlobalMessages.ERROR_GET, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
                

    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create():
        data = request.get_json()
        with get_db() as db:
            try:
                service = BudgetTimelineService(db)
                budget = service.create(data)
                
                return jsonify(serialize_model(budget)), 201
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            

    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Presupuesto")
    def update(budget_timeline_id: int):
        data = request.get_json()
        with get_db() as db:
            try:
                service = BudgetTimelineService(db)
                budget = service.update(budget_timeline_id, data)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(serialize_model(budget))
            except Exception as e:
                return http_response(GlobalMessages.ERROR_UPDATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            


    @require_auth
    @staticmethod
    @require_permission("Eliminar", "Presupuesto")
    def delete(budget_timeline_id: int):
        with get_db() as db:
            try:
                service = BudgetTimelineService(db)
                budget = service.delete(budget_timeline_id)
                if not budget:
                    abort(404, description="Budget not found")
                return jsonify({"message": "Budget deleted"})
            except Exception as e:
                return http_response(GlobalMessages.ERROR_DELETED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
                
                
                
    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create_massive():
        data = request.json
        try:
            with get_db() as db:
                service = BudgetTimelineService(db)
                budget = service.create_massive(data.get('budget_timeline'))
                return jsonify(budget)
                
        except Exception as e:
            return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            