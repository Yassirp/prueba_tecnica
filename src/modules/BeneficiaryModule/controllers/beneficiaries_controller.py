from flask import  jsonify
from modules.BeneficiaryModule.services.beneficiary_services import BeneficiaryService
from utils.serialize import serialize_model
from utils.request_utils import get_pagination_params, paginated_response, get_filter_params, http_response
from utils.global_message import GlobalMessages
from http import HTTPStatus
from database.database import get_db_mysql
from middleware.auth import require_auth
from utils.permission import require_permission


class BeneficiaryController:

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Beneficiarios")
    def get_all():
        try:
            limit, offset, order_by = get_pagination_params()
            filter = get_filter_params()
            with get_db_mysql() as db:
                service = BeneficiaryService(db)
                beneficiaries, total = service.get_all(limit=limit, offset=offset, order_by=order_by, filters= filter)
            
                return jsonify(paginated_response(beneficiaries, total, limit, offset, serialize_model)), 200
        except Exception as e:
            return http_response(GlobalMessages.ERROR_GET_ALL, {}, [str(e)], HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    @require_auth
    @require_permission("Acceder", "Beneficiarios")
    def get_All_with_relationship():
        with get_db_mysql() as db:
            service = BeneficiaryService(db)
            filters = get_filter_params()
            limit, offset, order_by = get_pagination_params()
            beneficiaries, total = service.get_all_with_relationship(limit, offset, order_by, filters)
                
            return jsonify(paginated_response(beneficiaries, total, limit, offset)), 200