from modules.BeneficiaryModule.repositories.beneficiary_repository import BeneficiaryRepository
from modules.BeneficiaryModule.schemas.beneficiary_schema import BeneficiaryUpdate,BeneficiaryCreate
from modules.BeneficiaryModule.models.beneficiaries import Beneficiary
from services.base_services import BaseService
from modules.BudgetModule.repositories.budget_repository import OBudgetRepository
from utils.structure.beneficiary_structure import structure_beneficiary
from modules.BeneficiaryModule.repositories.diagnostic_repository import DiagnosticRepository
from modules.BeneficiaryModule.repositories.document_repository import DocumentRepository
from database.database import get_db
from flask import  request

class BeneficiaryService(BaseService):
    def __init__(self, db):
        self.db = db
        self.diagnostic= DiagnosticRepository(db)
        self.documents= DocumentRepository(db)
        self.repo = BeneficiaryRepository(db)
        super().__init__(
            Beneficiary,
            self.repo,
            BeneficiaryCreate,
            BeneficiaryUpdate
        )
        
        with get_db() as db_pgsql:
            self.budget = OBudgetRepository(db_pgsql)
        



    def get_all_with_relationship(self,limit, offset, order_by, filters):
        try:
            user = getattr(request, "user", None)
            filters['process'] = 'Pre Aprobado'
            items, total = self.repo.get_all_with_relationships(limit, offset, order_by, filters,user)
            results = []
            for item in items:
                beneficiary, contrato_assignment,contract,department,municipality = item
                if beneficiary:
                    budget = self.budget.get_budget_by_beneficiary(beneficiary.id)
                    setattr(beneficiary, 'budget_id', budget.id if budget else None)

                diagnostic= self.diagnostic.get_by_beneficiary_id(beneficiary.id)
                documents=[]
                if diagnostic:
                    documents=  self.documents.get_by_associate_and_document_types([300,400], 'Diagnostic', diagnostic.id)

                data = structure_beneficiary(beneficiary,contrato_assignment,contract,department,municipality,documents)
                results.append(data)
            
            return results, total
            
        except Exception as e:
            raise Exception(f"Error al obtener los beneficiarios: {str(e)}")
