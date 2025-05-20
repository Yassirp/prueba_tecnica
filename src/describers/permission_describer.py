from typing import List
from sqlalchemy.orm import Session
from modules.PermissionModule.models.m_role import MRole as Role
from modules.PermissionModule.models.m_actions import MAction
from modules.PermissionModule.models.m_module import MModule
from modules.PermissionModule.models.c_module_actions import CModuleAction

class PermissionDescriber:
    def __init__(self, db: Session):
        self.db = db

    def describe_permissions(self, permissions: List[dict]) -> List[str]:
        descriptions = []

        for perm in permissions:
            role = self._get_role_name(perm.associate_id)
            action, module = self._get_action_and_module(perm.action_id)

            description = f"Rol: '{role}' tiene permiso de '{action}' en el módulo '{module}'"
            descriptions.append(description)

        return descriptions

    def _get_role_name(self, role_id: int) -> str:
        role = self.db.query(Role).filter_by(id=role_id).first()
        return role.name if role else f"Rol ID {role_id} no encontrado"

    def _get_action_and_module(self, action_id: int) -> tuple:
        cma = self.db.query(CModuleAction).filter_by(action_id=action_id).first()

        if not cma:
            return (f"Acción ID {action_id} no encontrada", "Módulo desconocido")

        action = self.db.query(MAction).filter_by(id=cma.action_id).first()
        module = self.db.query(MModule).filter_by(id=cma.module_id).first()

        action_name = action.name if action else f"Acción ID {cma.action_id} no encontrada"
        module_name = module.name if module else f"Módulo ID {cma.module_id} no encontrado"

        return (action_name, module_name)
