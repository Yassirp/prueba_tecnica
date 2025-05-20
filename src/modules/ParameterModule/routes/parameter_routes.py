from flask import Blueprint
from modules.ParameterModule.controllers.parameter_controller import ParameterController

parameter_bp = Blueprint('parameter', __name__)

parameter_bp.get('/parameters')(ParameterController.get_all_parameters)
parameter_bp.get('/parameter/<int:parameter_id>')(ParameterController.get_parameter_by_id)
parameter_bp.post('/create-parameter')(ParameterController.create_parameter)
parameter_bp.put('/update-parameter/<int:parameter_id>')(ParameterController.update_parameter)
parameter_bp.delete('/delete-parameter/<int:parameter_id>')(ParameterController.delete_parameter)
