from flask import  jsonify, request, abort
from modules.BudgetModule.services.budget_state_change_services import BudgetStatusChangeService
from utils.permission import require_permission
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params, http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from middleware.auth import require_auth
from database.database import get_db
from modules.BudgetModule.services.budget_services import OBudgetService

class BudgetStateChangeController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def get_all():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = BudgetStatusChangeService(db)
                budgets, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters= filter)
            
                return jsonify(paginated_response(budgets, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def get(budget_state_id: int):
        with get_db() as db:
            try:
                service = BudgetStatusChangeService(db)
                budget = service.get_by_id(budget_state_id)
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
                service = BudgetStatusChangeService(db)
                budget = service.create(data)
                
                return jsonify(serialize_model(budget)), 201
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create_budget_state():
        # pass
        data = request.get_json()
        with get_db() as db:
            try:
                service = BudgetStatusChangeService(db)
                service_budget = OBudgetService(db)
                budget_state_change = service.create(data)
                data={}
                if budget_state_change:
                    data['budget'] = serialize_model(service_budget.update(budget_state_change.budget_id, {'status_id': budget_state_change.status_id}))
                data['budget_state_change'] = serialize_model(budget_state_change)
                return jsonify(data), 201
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            

    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Presupuesto")
    def update(budget_state_id: int):
        data = request.get_json()
        with get_db() as db:
            try:
                service = BudgetStatusChangeService(db)
                budget = service.update(budget_state_id, data)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(serialize_model(budget))
            except Exception as e:
                return http_response(GlobalMessages.ERROR_UPDATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            


    @require_auth
    @staticmethod
    @require_permission("Eliminar", "Presupuesto")
    def delete(budget_state_id: int):
        with get_db() as db:
            try:
                service = BudgetStatusChangeService(db)
                budget = service.delete(budget_state_id)
                if not budget:
                    abort(404, description="Budget not found")
                return jsonify({"message": "Budget deleted"})
            except Exception as e:
                return http_response(GlobalMessages.ERROR_DELETED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
                