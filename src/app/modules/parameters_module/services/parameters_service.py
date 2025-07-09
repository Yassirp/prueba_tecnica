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
        
    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ):
        try:
            return await self.repo.get_all(limit, offset, order_by, filters)
        except Exception as e:
            raise e

    async def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = "id:asc", filters: dict = {}) -> tuple:
        try:
            return await self.repo.get_all_with_relationships(limit, offset, order_by, filters)
        except Exception as e:
            raise e

    async def get_by_id(self, entity_id: int) -> Optional[Parameter]:
        try:
            item = await self.repo.get_by_id(entity_id)
            return item
        except Exception as e:
            raise e