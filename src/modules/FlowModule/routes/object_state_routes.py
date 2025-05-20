from flask import Blueprint
from modules.FlowModule.controllers.object_state_controller import ObjectStateController

object_state_bp = Blueprint('object_states', __name__)


object_state_bp.get('/object-states')(ObjectStateController.get_object_states)
object_state_bp.get('/object-state/<int:object_state_id>')(ObjectStateController.get_object_state)
object_state_bp.post('/create-object-state')(ObjectStateController.create_object_state)
object_state_bp.put('/update-object-state/<int:object_state_id>')(ObjectStateController.update_object_state)
object_state_bp.delete('/delete-object-state/<int:object_state_id>')(ObjectStateController.delete_object_state)
