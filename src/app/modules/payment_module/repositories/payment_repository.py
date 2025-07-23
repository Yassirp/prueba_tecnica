
# Archivo generado automáticamente para sedes - repositories
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.payment_module.models.payment import Payment
from src.app.shared.bases.base_repository import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, model: type[Payment], db_session: AsyncSession):
        super().__init__(model, db_session)
        