from typing import Type, TypeVar, List, Optional, Dict, Any, Generic, Tuple
from .base_repository import BaseRepository
from pydantic import BaseModel

Model = TypeVar("Model")
OutSchema = TypeVar("OutSchema", bound=BaseModel)

class BaseService(Generic[Model, OutSchema]):
    def __init__(
        self,
        model: Type[Model],
        repository_cls: Type[BaseRepository],
        db_session,
        out_schema: Type[OutSchema]
    ):
        self.model = model
        self.repo = repository_cls(db_session)
        self.out_schema = out_schema

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict], int]:
        items, total = await self.repo.get_all(limit, offset, order_by, filters)
        serialized_items = [self.out_schema.model_validate(item).model_dump() for item in items]
        return serialized_items, total
    
    async def get_by_id(self, entity_id: int) -> Optional[Dict]:
        item = await self.repo.get_by_id(entity_id)
        if not item:
            return None
        return self.out_schema.model_validate(item).model_dump()

    async def create(self, data: dict) -> Dict:
        item = await self.repo.create(data)
        return self.out_schema.model_validate(item).model_dump()

    async def update(self, entity_id: int, data: dict) -> Optional[Dict]:
        item = await self.repo.update(entity_id, data)
        if not item:
            return None
        return self.out_schema.model_validate(item).model_dump()

    async def delete(self, entity_id: int) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if not entity:
            return False
        await self.repo.delete(entity.id)
        return True

    def _serialize_model(self, model: Model) -> dict:
        """Convierte un modelo SQLAlchemy a un diccionario"""
        if hasattr(model, '__dict__'):
            return {k: v for k, v in model.__dict__.items() if not k.startswith('_')}
        return {}
