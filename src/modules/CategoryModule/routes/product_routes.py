from flask import Blueprint
from modules.CategoryModule.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

product_bp.get('/products')(ProductController.get_all_products)
product_bp.get('/products-with-relationship')(ProductController.get_all_products_with_relationship)
product_bp.get('/product/<int:product_id>')(ProductController.get_product_by_id)
product_bp.post('/create-product')(ProductController.create_product)
product_bp.put('/update-product/<int:product_id>')(ProductController.update_product)
product_bp.delete('/delete-product/<int:product_id>')(ProductController.delete_product)
