from modules.ParameterModule.models.m_parameters import MParameter
from modules.ParameterModule.schemas.parameter_schema import MParameterCreate, MParameterUpdate
from modules.ParameterModule.repositories.parameter_repository import ParameterRepository
from services.base_services import BaseService
class ParameterService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = ParameterRepository(db)
        super().__init__(
            MParameter,
            self.repo,
            MParameterCreate,
            MParameterUpdate
        )
        