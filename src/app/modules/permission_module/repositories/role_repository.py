from modules.PermissionModule.models.m_role import MRole
from repositories.base_repository import BaseRepository
from modules.PermissionModule.models.c_permissions import CPermission
from modules.PermissionModule.models.c_module_actions import CModuleAction
from sqlalchemy.orm import Session, selectinload

class RoleRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, MRole)

    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'id:asc', filters: dict = None):
        # Inicia la consulta con MRole
        query = self.db.query(MRole)
        # Log de la consulta inicial

        # Usar selectinload para cargar las relaciones de manera más eficiente
        query = query.options(
            selectinload(MRole.permissions)
            .selectinload(CPermission.module_action)
            .selectinload(CModuleAction.module),
            selectinload(MRole.permissions)
            .selectinload(CPermission.module_action)
            .selectinload(CModuleAction.action)
        )

        # Filtrar si hay filtros
        if filters:
            query = self.filter_by(query, filters)

        # Ordenar si hay orden
        if order_by:
            query = self.order_by(query, order_by)

        # Obtener total de registros
        total = query.count()

        # Limitar y paginar
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        # Recuperar los resultados
        roles = query.all()

        # Mapear los resultados para asegurarse de que las relaciones se devuelvan correctamente
        results = []
        for role in roles:
            role_data = {
                "id": getattr(role, "id", None),
                "code": getattr(role, "code", None),
                "name": getattr(role, "name", None),
                "created_at": getattr(role, "created_at", None),
                "updated_at": getattr(role, "updated_at", None),
                "permissions": [
                    {
                        "id": getattr(permission, "id", None),
                        "action_id": getattr(permission, "action_id", None),
                        "module_action": {
                            "id": getattr(getattr(permission, "module_action", None), "id", None),
                            "module": {
                                "id": getattr(getattr(getattr(permission, "module_action", None), "module", None), "id", None),
                                "name": getattr(getattr(getattr(permission, "module_action", None), "module", None), "name", None),
                                "level": getattr(getattr(getattr(permission, "module_action", None), "module", None), "level", None),
                                "parent_id": getattr(getattr(getattr(permission, "module_action", None), "module", None), "parent_id", None),
                                "path": getattr(getattr(getattr(permission, "module_action", None), "module", None), "path", None),
                                "position": getattr(getattr(getattr(permission, "module_action", None), "module", None), "position", None),
                                "icon": getattr(getattr(getattr(permission, "module_action", None), "module", None), "icon", None),
                            } if getattr(getattr(permission, "module_action", None), "module", None) else None,
                            "action": {
                                "id": getattr(getattr(getattr(permission, "module_action", None), "action", None), "id", None),
                                "name": getattr(getattr(getattr(permission, "module_action", None), "action", None), "name", None),
                            } if getattr(getattr(permission, "module_action", None), "action", None) else None,
                        } if getattr(permission, "module_action", None) else None,
                    } for permission in getattr(role, "permissions", []) or []
                ]
            }
            results.append(role_data)

        return results, total
