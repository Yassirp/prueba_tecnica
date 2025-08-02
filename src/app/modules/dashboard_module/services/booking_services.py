from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.bases.base_service import BaseService
from app.modules.dashboard_module.models.bookings import Booking
from app.modules.dashboard_module.repositories.booking_repository import BookingRepository
from app.modules.dashboard_module.schemas.booking_schemas import BookingOut

class BookingService(BaseService[Booking, BookingOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = BookingRepository(Booking, self.db_session)
        super().__init__(
            model=Booking,
            repository_cls=BookingRepository,
            db_session=self.db_session,
            out_schema=BookingOut,
        ) 