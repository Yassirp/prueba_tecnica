from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.contract_assignments import ContratoAssignment



class  ContractAssignmentRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = ContratoAssignment
        super().__init__(self.db, self.model)



    def get_by_associate_id_and_associate_to(self, associate_to: str, associate_id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.associate_id == associate_id)
            .filter(self.model.associate_to == associate_to)
            .first()
        )