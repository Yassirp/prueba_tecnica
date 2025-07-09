from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, Tuple
from src.app.modules.ubication_module.models.countries import Country
from src.app.modules.ubication_module.repositories.country_repository import CountryRepository
from src.app.modules.ubication_module.schemas.country_schemas import CountryOut
from src.app.shared.bases.base_service import BaseService

class CountryService(BaseService[Country, CountryOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Country,
            repository_cls=CountryRepository,
            db_session=db_session,
            out_schema=CountryOut,
        )
        
    async def get_all_countries(self, limit: int = 10, offset: int = 0, order_by: str = "id:asc", filters: dict = {}) -> tuple:
        countries, total = await self.repo.get_all_with_relationships(limit, offset, order_by, filters)
        return countries, total
        