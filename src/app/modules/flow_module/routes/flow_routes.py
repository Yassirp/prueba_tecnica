from flask import Blueprint
from modules.FlowModule.controllers.flow_controller import FlowController

flow_bp = Blueprint('flows', __name__)


flow_bp.get('/flows')(FlowController.get_flows)
flow_bp.get('/flow/<int:flow_id>')(FlowController.get_flow)
flow_bp.post('/create-flow')(FlowController.create_flow)
flow_bp.put('/update-flow/<int:flow_id>')(FlowController.update_flow)
flow_bp.delete('/delete-flow/<int:flow_id>')(FlowController.delete_flow)
