from flask import Blueprint
from modules.UserModule.controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)



user_bp.get('/users')(UserController.get_all_users)
user_bp.get('/user/<int:user_id>')(UserController.get_user_by_id)