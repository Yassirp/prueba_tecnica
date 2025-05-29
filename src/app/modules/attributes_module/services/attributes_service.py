# Archivo generado automáticamente para attributes - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.attributes_module.repositories.attributes_repository import AttributeRepository
from src.app.modules.attributes_module.schemas.attributes_schemas import AttributeOut
from src.app.shared.bases.base_service import BaseService
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class AttributeService(BaseService[Attribute, AttributeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Attribute,
            repository_cls=AttributeRepository,
            db_session=db_session,
            out_schema=AttributeOut,
        )
        self.db_session = db_session

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(selectinload(self.model.parameter))

            # Aquí puedes aplicar filtros, orden y paginación si los necesitas.
            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)
            
            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()

            # Opcional: Si tienes filtros aplicados en SQL puedes contar antes,
            # si no, simplemente haces len().
            total = len(items)
            return items, total
        except Exception as e:
            raise e