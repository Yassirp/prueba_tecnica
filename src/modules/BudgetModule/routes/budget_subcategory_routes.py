from flask import Blueprint
from modules.BudgetModule.controllers.budget_subcategory_controller import BudgetSubcategoryController

budget_subcategory_bp = Blueprint('budget_subcategory', __name__)


budget_subcategory_bp.get('/budget-subcategories')(BudgetSubcategoryController.get_all)
budget_subcategory_bp.get('/budget-subcategory/<int:budget_subcategory_id>')(BudgetSubcategoryController.get)
budget_subcategory_bp.post('/create-budget-subcategory')(BudgetSubcategoryController.create)
budget_subcategory_bp.put('/update-budget-subcategory/<int:budget_subcategory_id>')(BudgetSubcategoryController.update)
budget_subcategory_bp.delete('/delete-budget-subcategory/<int:budget_subcategory_id>')(BudgetSubcategoryController.delete)
