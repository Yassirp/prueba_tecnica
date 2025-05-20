from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.municipalities import Municipality


class  MunicipalityRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = Municipality
        super().__init__(self.db, self.model)

