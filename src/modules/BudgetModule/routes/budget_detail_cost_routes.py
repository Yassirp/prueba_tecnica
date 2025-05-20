from flask import Blueprint
from modules.BudgetModule.controllers.budget_detail_cost_controller import BudgetDetailCostController

budget_detail_cost_bp = Blueprint('budget_detail_cost', __name__)


budget_detail_cost_bp.get('/budget-detail-costs')(BudgetDetailCostController.get_all)
budget_detail_cost_bp.get('/budget-detail-cost/<int:budget_detail_cost_id>')(BudgetDetailCostController.get)
budget_detail_cost_bp.post('/create-budget-detail-cost')(BudgetDetailCostController.create)
budget_detail_cost_bp.put('/update-budget-detail-cost/<int:budget_detail_cost_id>')(BudgetDetailCostController.update)
budget_detail_cost_bp.delete('/delete-budget-detail-cost/<int:budget_detail_cost_id>')(BudgetDetailCostController.delete)
