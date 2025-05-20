from flask import Blueprint
from modules.BudgetModule.controllers.budget_subcategory_detail_controller import BudgetSubcategoryDetailController

budget_subcategory_detail_bp = Blueprint('budget_subcategory_detail', __name__)


budget_subcategory_detail_bp.get('/budget-subcategories-details')(BudgetSubcategoryDetailController.get_all)
budget_subcategory_detail_bp.get('/budget-subcategory-detail/<int:budget_subcategory_detail_id>')(BudgetSubcategoryDetailController.get)
budget_subcategory_detail_bp.post('/create-budget-subcategory-detail')(BudgetSubcategoryDetailController.create)
budget_subcategory_detail_bp.put('/update-budget-subcategory-detail/<int:budget_subcategory_detail_id>')(BudgetSubcategoryDetailController.update)
budget_subcategory_detail_bp.delete('/delete-budget-subcategory-detail/<int:budget_subcategory_detail_id>')(BudgetSubcategoryDetailController.delete)
