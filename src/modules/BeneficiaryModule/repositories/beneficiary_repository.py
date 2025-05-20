from sqlalchemy.orm import Session
from modules.BeneficiaryModule.models.beneficiaries import Beneficiary
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.contract_assignments import ContratoAssignment
from modules.BeneficiaryModule.models.contracts import Contract
from modules.BeneficiaryModule.models.departments import Department
from modules.BeneficiaryModule.models.municipalities import Municipality
class  BeneficiaryRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = Beneficiary
        super().__init__(self.db, self.model)


    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None, user = None) -> list[Beneficiary]:
        
        query = self.db.query(self.model, ContratoAssignment, Contract,Department,Municipality) \
        .join(ContratoAssignment, self.model.id == ContratoAssignment.associate_id) \
        .join(Contract, ContratoAssignment.id_contrato == Contract.id) \
        .join(Department, Department.id ==  self.model.departament) \
        .join(Municipality, Municipality.id ==  self.model.municipality) \
        .filter(ContratoAssignment.associate_to == 'Beneficiario')

        if user and getattr(user, "old_id", None) == 3:
            query = query.filter(ContratoAssignment.parent_id == getattr(user, "id", None))
            
        if filters:
            query = self.filter_by(query, filters)

        if order_by:
            query = self.order_by(query, order_by)

        total = query.count()
        
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)


        items = query.all()
                    
        return items, total
        