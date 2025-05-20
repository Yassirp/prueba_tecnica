from flask import Blueprint
from modules.ParameterModule.controllers.pv_controller import PVController

pv_bp = Blueprint('parameter_value', __name__)

pv_bp.get('/parameter-values')(PVController.get_all_parameter_values)
pv_bp.post('/parameter-value-with-parameter')(PVController.get_all_parameter_values_by_parameter_reference)
pv_bp.get('/parameter-value/<int:pv_id>')(PVController.get_parameter_value_by_id)
pv_bp.post('/create-parameter-value')(PVController.create_parameter_value)
pv_bp.put('/update-parameter-value/<int:pv_id>')(PVController.update_parameter_value)
pv_bp.delete('/delete-parameter-value/<int:pv_id>')(PVController.delete_parameter_value)
