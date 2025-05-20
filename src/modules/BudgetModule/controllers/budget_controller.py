from flask import  jsonify, request, abort
from modules.BudgetModule.services.budget_services import OBudgetService
from utils.permission import require_permission
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params, http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from middleware.auth import require_auth
from database.database import get_db


class BudgetController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def list_budgets():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = OBudgetService(db)
                budgets, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters= filter)
            
                return jsonify(paginated_response(budgets, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)


    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")
    def get_budget(budget_id: int):
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.get_by_id(budget_id)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(serialize_model(budget))
            except Exception as e:
                return http_response(GlobalMessages.ERROR_GET, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
                

    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create_budget():
        data = request.get_json()
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.create(data)
                
                return jsonify(serialize_model(budget)), 201
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            

    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Presupuesto")
    def update_budget(budget_id: int):
        data = request.get_json()
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.update(budget_id, data)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(serialize_model(budget))
            except Exception as e:
                return http_response(GlobalMessages.ERROR_UPDATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            


    @require_auth
    @staticmethod
    @require_permission("Eliminar", "Presupuesto")
    def delete_budget(budget_id: int):
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.delete(budget_id)
                if not budget:
                    abort(404, description="Budget not found")
                return jsonify({"message": "Budget deleted"})
            except Exception as e:
                return http_response(GlobalMessages.ERROR_DELETED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
    
    
    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create_budget_with_details():
        data = request.get_json()
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.create_budget_with_details(data)
                
                return jsonify(budget), 201
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
    
    
    
    @require_auth
    @staticmethod
    @require_permission("Crear", "Presupuesto")
    def create_budget_with_quantity():
        data = request.get_json()
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget_quantity = service.create_budget_with_quantity(data)
                
                return jsonify(budget_quantity), 201
            
            except Exception as e:
                return http_response(GlobalMessages.ERROR_CREATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
            
    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Presupuesto")
    def update_budget_with_quantity(budget_id: int):
        data = request.get_json()
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget = service.update_budget_with_quantity(budget_id, data)
                if not budget:
                    return jsonify({'error': 'Budget not found'}), 404
                return jsonify(budget)
            except Exception as e:
                return http_response(GlobalMessages.ERROR_UPDATED, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
            
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")     
    def get_all_with_relationships():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db() as db:
                service = OBudgetService(db)
                budgets, total = service.get_all_with_relationships(limit=limit, offset=offset, order_by=order_by, filters= filter)
                
                return jsonify(paginated_response(budgets, total, limit, offset)), 200
                
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
            
    @staticmethod
    @require_auth
    @require_permission("Acceder", "Presupuesto")    
    def get_budget_with_relationship(budget_id):
        with get_db() as db:
            try:
                service = OBudgetService(db)
                budget_quantity = service.get_with_relationships(budget_id)
                
                return jsonify(budget_quantity), 201
            
            except Exception as e:
                return http_response(GlobalMessages.ERROR_GET, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)
             
                
                
    @require_auth
    @staticmethod
    @require_permission("Actualizar", "Presupuesto")
    def update_budgets_and_state():
        with get_db() as db:
            data = request.get_json()

            budget_ids = data.get("budget_ids")
            status_id = data.get("status_id")
            user_id = request.get("user_id")

            try:
                service = OBudgetService(db)
                result = service.update_budgets_and_state(budget_ids, status_id, user_id)
                return jsonify(result), 200

            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400

            except Exception as e:
                return http_response(
                    GlobalMessages.ERROR_UPDATED,
                    {},
                    [str(e)],
                    HTTPStatus.INTERNAL_SERVER_ERROR
                )