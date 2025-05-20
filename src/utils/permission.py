from functools import wraps
from flask import request, jsonify
from modules.PermissionModule.models.c_permissions import CPermission
from modules.PermissionModule.models.c_module_actions import CModuleAction
from modules.PermissionModule.models.m_module import MModule
from modules.PermissionModule.models.m_actions import MAction
from modules.PermissionModule.models.m_role import MRole



def require_permission(action: str, module: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db = request.db  
            user = getattr(request, "user", None)
            if not user:
                return jsonify({"error": "Usuario no autenticado"}), 401


            if user.old_id == 1:
                return func(*args, **kwargs)
            
            role_entity = db.query(MRole).filter_by(old_id=user.old_id).first()
            if not role_entity:
                return jsonify({"error": "Rol no encontrado"}), 403
            action_entity = db.query(MAction).filter_by(name=action).first()
            module_entity = db.query(MModule).filter_by(name=module).first()
            if not action_entity or not module_entity:
                return jsonify({"error": "Acción o módulo no encontrados"}), 400

            modules_action = db.query(CModuleAction).filter_by(
                action_id=action_entity.id,
                module_id=module_entity.id
            ).first()

            if not modules_action:
                return jsonify({"error": "Permiso no configurado"}), 403

            # Consultar permisos por rol o usuario
            permission = db.query(CPermission).filter(
                CPermission.action_id == modules_action.id,
                ((CPermission.associate_to == 'users') & (CPermission.associate_id == user.id)) |
                ((CPermission.associate_to == 'roles') & (CPermission.associate_id == role_entity.id))
            ).first()

            if not permission:
                return jsonify({"error": f"No tiene permiso de '{action}' en '{module}'"}), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator
