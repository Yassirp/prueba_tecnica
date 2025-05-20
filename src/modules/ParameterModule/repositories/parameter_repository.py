from modules.ParameterModule.models.m_parameters import MParameter
from repositories.base_repository import BaseRepository
class ParameterRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MParameter)


