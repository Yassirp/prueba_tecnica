from typing import Type, TypeVar, List, Optional, Dict, Any
from app.shared.bases.base_repository import BaseRepository
from pydantic import ValidationError
from fastapi import HTTPException

Model = TypeVar("Model")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")

class BaseService:
    def __init__(
        self,
        model: Type[Model],
        repository_cls: Type[BaseRepository],
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        db_session
    ):
        self.model = model
        self.repo = repository_cls(db_session)
        self.create_schema = create_schema
        self.update_schema = update_schema

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Model]:
        return await self.repo.get_all(limit, offset, order_by, filters)
    
    async def get_by_id(self, entity_id: int) -> Optional[Model]:
        return await self.repo.get_by_id(entity_id)

    async def create(self, data: dict) -> Model:
        try:
            validated_data = self.create_schema.model_validate(data, context={'db': self.repo.db})
        except ValidationError as ve:
            raise HTTPException(status_code=422, detail=ve.errors())

        return await self.repo.create(validated_data.model_dump())

    async def update(self, entity_id: int, data: dict) -> Model:
        try:
            validated_data = self.update_schema.model_validate(data, context={'db': self.repo.db, 'id': entity_id})
        except ValidationError as ve:
            raise HTTPException(status_code=422, detail=ve.errors())

        return await self.repo.update(entity_id, validated_data.model_dump(exclude_unset=True))

    async def delete(self, entity_id: int) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if not entity:
            return False
        await self.repo.delete(entity.id)
        return True
