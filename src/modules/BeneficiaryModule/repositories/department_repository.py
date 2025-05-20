from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.departments import Department

class  DepartmentRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = Department
        super().__init__(self.db, self.model)

