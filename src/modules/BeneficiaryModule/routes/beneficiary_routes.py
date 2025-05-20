from flask import Blueprint
from modules.BeneficiaryModule.controllers.beneficiaries_controller import BeneficiaryController

beneficiary_bp = Blueprint('beneficiary', __name__)


beneficiary_bp.get('/beneficiaries')(BeneficiaryController.get_all)
beneficiary_bp.get('/beneficiaries-with-relationship')(BeneficiaryController.get_All_with_relationship)