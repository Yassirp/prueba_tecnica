from flask import Blueprint
from modules.BudgetModule.controllers.budget_controller import BudgetController

budget_bp = Blueprint('budgets', __name__)


budget_bp.get('/budgets')(BudgetController.list_budgets)
budget_bp.get('/budget/<int:budget_id>')(BudgetController.get_budget)
budget_bp.get('/budget-with-relationship/<int:budget_id>')(BudgetController.get_budget_with_relationship)
budget_bp.get('/budgets-with-relationship')(BudgetController.get_all_with_relationships)
budget_bp.post('/create-budget')(BudgetController.create_budget)
budget_bp.put('/update-budget/<int:budget_id>')(BudgetController.update_budget)
budget_bp.put('/update-budget/categories/subcategories/quantity/<int:budget_id>')(BudgetController.update_budget_with_quantity)
budget_bp.delete('/delete-budget/<int:budget_id>')(BudgetController.delete_budget)
budget_bp.post('/create-budget/categories/subcategories/details')(BudgetController.create_budget_with_details)
budget_bp.post('/create-budget/categories/subcategories/quantity')(BudgetController.create_budget_with_quantity)
budget_bp.patch('/update-budgets-status')(BudgetController.update_budgets_and_state)