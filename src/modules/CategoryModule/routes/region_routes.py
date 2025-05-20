from flask import Blueprint
from modules.CategoryModule.controllers.region_controller import RegionController

region_bp = Blueprint('regions', __name__)

region_bp.route('/regions', methods=['GET'])(RegionController.get_all)
region_bp.route('/region/<int:region_id>', methods=['GET'])(RegionController.get_one)
region_bp.route('/regions-with-relationship', methods=['GET'])(RegionController.get_all_with_relationship)
region_bp.route('/create-region', methods=['POST'])(RegionController.create)
region_bp.route('/update-region/<int:region_id>', methods=['PUT'])(RegionController.update)
region_bp.route('/delete-region/<int:region_id>', methods=['DELETE'])(RegionController.delete)
