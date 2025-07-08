from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, Tuple
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.modules.parameters_module.repositories.parameters_repository import ParameterRepository
from src.app.modules.parameters_module.schemas.parameters_schemas import ParameterOut
from src.app.shared.bases.base_service import BaseService
from src.app.modules.parameters_module.schemas.parameter_values_schemas import ParameterValueOut

class ParameterService(BaseService[Parameter, ParameterOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Parameter,
            repository_cls=ParameterRepository,
            db_session=db_session,
            out_schema=ParameterOut,
        )

    def serialize_param_value(self, value):
        return {
            'id': value.id,
            'parameter_id': value.parameter_id,
            'reference': value.reference,
            'value': value.value,
            'description': value.description,
            'parent_id': value.parent_id,
            'state': value.state,
            'created_at': value.created_at,
            'updated_at': value.updated_at,
            'deleted_at': value.deleted_at,
            'children': [self.serialize_param_value(child) for child in getattr(value, 'children', []) or []]
        }

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            items, total = await self.repo.get_all(limit, offset, order_by, filters)
            serialized_items = []
            for item in items:
                item_dict = {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'state': item.state,
                    'reference': getattr(item, 'reference', None),
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                    'deleted_at': item.deleted_at,
                    'values': [self.serialize_param_value(value) for value in item.values] if item.values else None
                }
                serialized_items.append(item_dict)
            return serialized_items, total
        except Exception as e:
            raise e

    async def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        try:
            item = await self.repo.get_by_id(entity_id)
            if not item:
                return None
            item_dict = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'state': item.state,
                'reference': getattr(item, 'reference', None),
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'deleted_at': item.deleted_at,
                'values': [self.serialize_param_value(value) for value in item.values] if item.values else None
            }
            return item_dict
        except Exception as e:
            raise e