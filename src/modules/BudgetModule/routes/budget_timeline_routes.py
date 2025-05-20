from flask import Blueprint
from modules.BudgetModule.controllers.budget_timeline_controller import BudgetTimelineController

budget_timeline_bp = Blueprint('budget_timeline', __name__)


budget_timeline_bp.get('/budgets-timeline')(BudgetTimelineController.get_all)
budget_timeline_bp.get('/budget-timeline/<int:budget_timeline_id>')(BudgetTimelineController.get)
budget_timeline_bp.post('/create-budget-timeline')(BudgetTimelineController.create)
budget_timeline_bp.post('/create-budget-timeline-massive')(BudgetTimelineController.create_massive)
budget_timeline_bp.put('/update-budget-timeline/<int:budget_timeline_id>')(BudgetTimelineController.update)
budget_timeline_bp.delete('/delete-budget-timeline/<int:budget_timeline_id>')(BudgetTimelineController.delete)