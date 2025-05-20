from modules.PermissionModule.models.m_role import MRole
from repositories.base_repository import BaseRepository
from modules.PermissionModule.models.c_permissions import CPermission
from modules.PermissionModule.models.c_module_actions import CModuleAction
from sqlalchemy.orm import Session, joinedload

class RoleRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, MRole)

    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'id:asc', filters: dict = None):
        # Inicia la consulta con MRole
        query = self.db.query(MRole)
       # Log de la consulta inicial

        # Cargar relaciones
        query = query.options(
            joinedload(MRole.permissions)
            .joinedload(CPermission.module_action)
            .joinedload(CModuleAction.module),  # Relacionar con el módulo
            joinedload(MRole.permissions)
            .joinedload(CPermission.module_action)
            .joinedload(CModuleAction.action)  # Relacionar con la acción
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
                "id": role.id,
                "code": role.code,
                "name": role.name,
                "created_at": role.created_at,
                "updated_at": role.updated_at,
                "permissions": [
                    {
                        "id": permission.id,
                        "action_id": permission.action_id,
                        "module_action": {
                            "id": permission.module_action.id,
                            "module": {
                                "id": permission.module_action.module.id,
                                "name": permission.module_action.module.name,
                            },
                            "action": {
                                "id": permission.module_action.action.id,
                                "name": permission.module_action.action.name,
                            }
                        }
                    } for permission in role.permissions
                ]
            }
            results.append(role_data)

        return results, total
