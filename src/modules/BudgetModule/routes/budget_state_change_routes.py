from flask import Blueprint
from modules.BudgetModule.controllers.budget_state_change_controller import BudgetStateChangeController

budget_state_change_bp = Blueprint('budget_state_change', __name__)


budget_state_change_bp.get('/budget-status-change')(BudgetStateChangeController.get_all)
budget_state_change_bp.get('/budget-state-change/<int:budget_state_change_id>')(BudgetStateChangeController.get)
budget_state_change_bp.post('/create-budget-state-change')(BudgetStateChangeController.create)
budget_state_change_bp.put('/update-budget-state-change/<int:budget_state_change_id>')(BudgetStateChangeController.update)
budget_state_change_bp.delete('/delete-budget-state-change/<int:budget_state_change_id>')(BudgetStateChangeController.delete)

budget_state_change_bp.post('/create-budget-state-change-with-budget')(BudgetStateChangeController.create_budget_state)