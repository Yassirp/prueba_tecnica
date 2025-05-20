from modules.PermissionModule.models.m_module import MModule
from sqlalchemy.orm import  joinedload
from repositories.base_repository import BaseRepository
from modules.PermissionModule.models.c_module_actions import CModuleAction

class ModuleRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MModule)


    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None) -> list[MModule]:  
        
        query = self.db.query(MModule)
        
        query = query.options(
            joinedload(MModule.module_actions) 
            .joinedload(CModuleAction.action),
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
        items = query.all()
        
        results = []
        
        for item in items:
            data = {
                "id": item.id,
                "name": item.name,
                "actions": [
                    {
                        "module_action_id": action.id,
                        "id": action.action_id,
                        "name": action.action.name,
                    } for action in item.module_actions
                ]
            }
            
            results.append(data)
            
        return results, total
        