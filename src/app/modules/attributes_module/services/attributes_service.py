# Archivo generado automáticamente para attributes - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.attributes_module.repositories.attributes_repository import AttributeRepository
from src.app.modules.attributes_module.schemas.attributes_schemas import AttributeOut
from src.app.shared.bases.base_service import BaseService

class AttributeService(BaseService[Attribute, AttributeOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Attribute,
            repository_cls=AttributeRepository,
            db_session=db_session,
            out_schema=AttributeOut,
        )