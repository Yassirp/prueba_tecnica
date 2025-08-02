from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.bases.base_service import BaseService
from app.modules.soccer_field_module.models.soccer_fields import SoccerField
from app.modules.soccer_field_module.repositories.soccer_field_repository import SoccerFieldRepository
from app.modules.soccer_field_module.schemas.soccer_field_schemas import SoccerFieldOut

class SoccerFieldService(BaseService[SoccerField, SoccerFieldOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = SoccerFieldRepository(SoccerField, self.db_session)
        super().__init__(
            model=SoccerField,
            repository_cls=SoccerFieldRepository,
            db_session=self.db_session,
            out_schema=SoccerFieldOut,
        )