from flask import Blueprint
from modules.BudgetModule.controllers.budget_beneficiary_controller import BudgetBeneficiaryController

budget_beneficiary_bp = Blueprint('budget_beneficiary', __name__)


budget_beneficiary_bp.get('/budget-beneficiaries')(BudgetBeneficiaryController.get_all)
budget_beneficiary_bp.get('/budget-beneficiary/<int:budget_beneficiary_id>')(BudgetBeneficiaryController.get)
budget_beneficiary_bp.post('/create-budget-beneficiary')(BudgetBeneficiaryController.create)
budget_beneficiary_bp.put('/update-budget-beneficiary/<int:budget_beneficiary_id>')(BudgetBeneficiaryController.update)
budget_beneficiary_bp.delete('/delete-budget-beneficiary/<int:budget_beneficiary_id>')(BudgetBeneficiaryController.delete)
