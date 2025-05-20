from flask import Blueprint
from modules.CategoryModule.controllers.subcategory_controller import SubcategoryController

subcategory_bp = Blueprint('subcategory', __name__)

subcategory_bp.get('/subcategories')(SubcategoryController.get_all_subcategories)
subcategory_bp.get('/subcategories-with-relationship')(SubcategoryController.get_all_with_relationship)
subcategory_bp.get('/subcategory/<int:subcategory_id>')(SubcategoryController.get_subcategory_by_id)
subcategory_bp.get('/products/subcategory/<string:subcategory_apu>')(SubcategoryController.get_subcategory_products)
subcategory_bp.post('/create-subcategory')(SubcategoryController.create_subcategory)
subcategory_bp.put('/update-subcategory/<int:subcategory_id>')(SubcategoryController.update_subcategory)
subcategory_bp.delete('/delete-subcategory/<int:subcategory_id>')(SubcategoryController.delete_subcategory)
