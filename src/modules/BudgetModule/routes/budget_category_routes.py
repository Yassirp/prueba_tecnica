from flask import Blueprint
from modules.BudgetModule.controllers.budget_category_controller import BudgetCategoryController

budget_category_bp = Blueprint('budget_category', __name__)


budget_category_bp.get('/budget-categories')(BudgetCategoryController.get_all)
budget_category_bp.get('/budget-category/<int:budget_category_id>')(BudgetCategoryController.get)
budget_category_bp.post('/create-budget-category')(BudgetCategoryController.create)
budget_category_bp.put('/update-budget-category/<int:budget_category_id>')(BudgetCategoryController.update)
budget_category_bp.delete('/delete-budget-category/<int:budget_category_id>')(BudgetCategoryController.delete)
