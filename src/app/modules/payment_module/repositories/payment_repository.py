
# Archivo generado automáticamente para sedes - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.payment_module.models.payment import Payment
from src.app.shared.bases.base_repository import BaseRepository
from sqlalchemy import select

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, model: type[Payment], db_session: AsyncSession):
        super().__init__(model, db_session)
        
    async def get_by_external_reference(self, external_reference: str):
        return await self.db_session.execute(select(self.model).where(self.model.external_reference == external_reference)).scalar_one_or_none()