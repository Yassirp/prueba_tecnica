from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.modules.parameters_module.repositories.parameters_repository import ParameterRepository
from src.app.modules.parameters_module.schemas.parameters_schemas import ParameterOut
from src.app.shared.bases.base_service import BaseService

class ParameterService(BaseService[Parameter, ParameterOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Parameter,
            repository_cls=ParameterRepository,
            db_session=db_session,
            out_schema=ParameterOut,
        )