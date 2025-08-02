from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.dashboard_module.models.bookings import Booking
from app.shared.bases.base_repository import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, model: type[Booking], db_session: AsyncSession):
        super().__init__(model, db_session) 