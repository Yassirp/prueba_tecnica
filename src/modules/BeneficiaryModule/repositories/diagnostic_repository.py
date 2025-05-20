from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.diagnostic import BeneficiaryIntegralDiagnostic



class  DiagnosticRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = BeneficiaryIntegralDiagnostic
        super().__init__(self.db, self.model)


    def get_by_beneficiary_id(self, beneficiary_id:int):
        return self.db.query(self.model).filter(self.model.beneficiary_id == beneficiary_id).first()

