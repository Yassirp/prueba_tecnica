from flask import Blueprint
from modules.CategoryModule.controllers.subcategory_detail_controller import SubcategoryDetailController

subcategory_detail_bp = Blueprint('subcategory_detail', __name__)

subcategory_detail_bp.get('/subcategories-details')(SubcategoryDetailController.get_all)
subcategory_detail_bp.get('/subcategory-detail/<int:subcategory_detail_id>')(SubcategoryDetailController.get_by_id)
subcategory_detail_bp.post('/create-subcategory-detail')(SubcategoryDetailController.create)
subcategory_detail_bp.put('/update-subcategory-detail/<int:subcategory_detail_id>')(SubcategoryDetailController.update)
subcategory_detail_bp.delete('/delete-subcategory-detail/<int:subcategory_detail_id>')(SubcategoryDetailController.delete)
