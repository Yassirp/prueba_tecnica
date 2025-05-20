from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.contracts import Contract



class  ContractRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = Contract
        super().__init__(self.db, self.model)

