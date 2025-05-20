from flask import Blueprint
from modules.CategoryModule.controllers.category_region_controller import CategoryRegionController

category_region_bp = Blueprint('category_region', __name__)

category_region_bp.get('/categories-regions')(CategoryRegionController.get_all)
category_region_bp.get('/category-region/<int:category_id>')(CategoryRegionController.get_by_id)
category_region_bp.get('/categories-regions-with-relationship')(CategoryRegionController.get_All_with_relationship)
category_region_bp.post('/create-category-region')(CategoryRegionController.create)
category_region_bp.put('/update-category-region/<int:category_id>')(CategoryRegionController.update)
category_region_bp.delete('/delete-category-region/<int:category_id>')(CategoryRegionController.delete)
category_region_bp.get('/region-category/<int:region_id>')(CategoryRegionController.get_subcategories_by_region)

# category_region_bp.post('/create-category-with-region')(CategoryRegionController.create_category_with_region)