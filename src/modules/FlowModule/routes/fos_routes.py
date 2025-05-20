from flask import Blueprint
from modules.FlowModule.controllers.flow_object_state_controller import FlowObjectStateController

flow_object_state_bp = Blueprint('flow_object_state', __name__)


flow_object_state_bp.get('/flow-object-states')(FlowObjectStateController.get_flows)
flow_object_state_bp.get('/flow-object-state/<int:flow_object_state_id>')(FlowObjectStateController.get_flow)
flow_object_state_bp.post('/create-flow-object-state')(FlowObjectStateController.create_flow)
flow_object_state_bp.put('/update-flow-object-state/<int:flow_object_state_id>')(FlowObjectStateController.update_flow)
flow_object_state_bp.delete('/delete-flow-object-state/<int:flow_object_state_id>')(FlowObjectStateController.delete_flow)
