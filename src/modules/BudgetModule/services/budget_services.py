from services.base_services import BaseService
from sqlalchemy.orm import Session
from modules.BudgetModule.schemas.budget_schema import OBudgetCreate, OBudgetUpdate
from modules.BudgetModule.repositories.budget_repository import OBudgetRepository
from modules.BudgetModule.services.budget_detail_cost_services import BudgetDetailCostService
from modules.BudgetModule.models.o_budgets import OBudget
from modules.BeneficiaryModule.repositories.contract_assignment_repository import ContractAssignmentRepository
from modules.BeneficiaryModule.repositories.contract_repository import ContractRepository
from modules.BeneficiaryModule.repositories.department_repository import DepartmentRepository
from modules.BeneficiaryModule.repositories.diagnostic_repository import DiagnosticRepository
from modules.BeneficiaryModule.repositories.document_repository import DocumentRepository
from modules.BeneficiaryModule.repositories.municipality_repository import MunicipalityRepository
from modules.BudgetModule.services.budget_category_services import BudgetCategoryService
from modules.BudgetModule.services.budget_quantity_detail_services import BudgetQuantityDetailService
from modules.BudgetModule.services.budget_subcategory_services import BudgetSubcategoryService
from modules.FlowModule.repositories.fos_repository import FOSRepository
from modules.BudgetModule.services.budget_state_change_services import BudgetStatusChangeService
from utils.serialize import serialize_model
from modules.BeneficiaryModule.repositories.beneficiary_repository import BeneficiaryRepository
from database.database import get_db_mysql
from utils.structure.budget_structure import structure_budget_data
import math
from flask import  request

class OBudgetService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        
        self.repository = OBudgetRepository(db)
        super().__init__(OBudget, self.repository, OBudgetCreate, OBudgetUpdate)
        self.budget_category_service = BudgetCategoryService(db)
        self.budget_quantity_service = BudgetQuantityDetailService(db)
        self.budget_subcategory_service = BudgetSubcategoryService(db)
        self.budget_detail_cost_service = BudgetDetailCostService(db)
        self.flow_object_state = FOSRepository(db)
        self.status_change = BudgetStatusChangeService(db)
        with get_db_mysql() as db_sql:
            self.db_mysql = db_sql
            self.beneficiary = BeneficiaryRepository(db_sql)
            self.department = DepartmentRepository(db_sql)
            self.contract = ContractRepository(db_sql)
            self.contract_assignment = ContractAssignmentRepository(db_sql)
            self.municipality= MunicipalityRepository(db_sql)
            self.diagnostic= DiagnosticRepository(db_sql)
            self.documents= DocumentRepository(db_sql)


    def create_budget_with_details(self, budget_data: dict):
        created_data = {
            "budget": None,
            "categories": [],
            "cost_details": []
        }
        try:
            budget = self.create(budget_data.get("budget"))
            created_data["budget"] = serialize_model(budget)

            created_data["categories"] = self.budget_category_service.create_budget_categories_with_subcategory(
                budget.id, budget_data.get("budget_categories", [])
            )
            created_data["cost_details"] = self.budget_detail_cost_service.create_budget_cost_details(
                budget.id, budget_data.get("budget_details", []))
                

            return created_data
        except Exception as e:
            self.repository.db.rollback()
            raise e

    def create_budget_with_quantity(self, budget_data: dict):
        created_data = {
            "budget": None,
        }
        try:
            budget_data_dict = {
                "code": budget_data.get("code"),
                "contractor_id": budget_data.get("contractor_id"),
                "contract_id": budget_data.get("contract_id"),
                "department_id": budget_data.get("department_id"),
                "municipality_id": budget_data.get("municipality_id"),
                "village": budget_data.get("village"),
                "beneficiary_id": budget_data.get("beneficiary_id"),
                "resolution_id": budget_data.get("resolution_id"),
                "improvement_type_id": budget_data.get("improvement_type_id"),
                "specific_improvement_id": budget_data.get("specific_improvement_id"),
                "valid_year": budget_data.get("valid_year"),
                "minimum_salary_id": budget_data.get("minimum_salary_id"),
                "presentation_date": budget_data.get("presentation_date"),
                "scheme_type_id": budget_data.get("scheme_type_id"),
                "legal_minimum_wages": budget_data.get("legal_minimum_wages"),
                "subtotal_direct_costs": budget_data.get("subtotal_direct_costs"), #total_subcategory_value
                "subtotal_indirect_costs": budget_data.get("subtotal_indirect_costs"), #total_subcategory_value x25%
                "total_diagnosis": budget_data.get("total_diagnosis"),
                "total_budget": budget_data.get("total_budget"),  #subtotal_indirect_costs + subtotal_direct_costs +  total_diagnosis
                # "status_id": budget_data.get("status_id"),
            }
            
            flow_object_state= self.flow_object_state.get_order_and_flow(1,1)
            if flow_object_state:
                budget_data_dict['status_id'] = flow_object_state.object_state_id
            budget = self.create(budget_data_dict)
            created_data["budget"] = serialize_model(budget)

            

            created_data["categories"] = self.budget_category_service.create_budget_categories_with_subcategory(
                budget.id, budget_data.get("categories", [])
            )
            total_subcategory_value = 0
            for category in created_data["categories"]:
                for subcategory in category.get("subcategories", []):
                    sub_value = subcategory.get("subcategory", {}).get("total_value")
                    if sub_value:
                        total_subcategory_value += float(sub_value)

            subtotal_direct_costs = math.ceil(total_subcategory_value)
            total_diagnosis = float(budget_data.get("total_diagnosis") or 0)
            admin = math.ceil(subtotal_direct_costs * 0.16)
            improve = math.ceil(subtotal_direct_costs * 0.02)
            utils= math.ceil(subtotal_direct_costs * 0.07)
            subtotal_indirect_costs = math.ceil(admin + improve+ utils)
            total_budget = subtotal_direct_costs + subtotal_indirect_costs + total_diagnosis
            
            cost_details= [
                {
                    "type_id": 82, 
                    "concept_id": 84, 
                    "value": admin,
                    "percentage": 16
                },
                {
                    "type_id": 82, 
                    "concept_id": 85, 
                    "value": improve,
                    "percentage": 2
                },
                {
                    "type_id": 82, 
                    "concept_id": 86, 
                    "value": utils,
                    "percentage": 7
                },
            ]


            created_data["cost_details"] = self.budget_detail_cost_service.create_budget_cost_details(
                budget.id, cost_details)
            
            # 4. Actualizar presupuesto con los valores calculados
            self.update(budget.id, {
                "subtotal_direct_costs": math.ceil(subtotal_direct_costs),
                "subtotal_indirect_costs": math.ceil(subtotal_indirect_costs),
                "total_budget": math.ceil(total_budget)
            })
            created_data["budget"]["subtotal_direct_costs"] = subtotal_direct_costs
            created_data["budget"]["subtotal_indirect_costs"] = subtotal_indirect_costs
            created_data["budget"]["total_budget"] = total_budget
            created_data["total_subcategories_value"] = total_subcategory_value

            return created_data
        except Exception as e:
            raise e


    def update_budget_with_quantity(self, budget_id: int, data: dict):
        pass
            
    def get_with_relationships(self, budget_id: int):
        try:
            budget = self.get_by_id(budget_id)
            if not budget:
                raise Exception("Presupuesto no encontrado")

            budget = self.repository.get_relationship_by_id(budget_id)

            beneficiary = self.beneficiary.get_by_id(budget.beneficiary_id)
            if not beneficiary:
                raise Exception("Beneficiario no encontrado")
            diagnostic= self.diagnostic.get_by_beneficiary_id(beneficiary.id)
            documents={}
            if diagnostic:
                documents=  self.documents.get_by_associate_and_document_types([300,400], 'Diagnostic', diagnostic.id)
                print(documents)
                        

            contract_assignment = self.contract_assignment.get_by_associate_id_and_associate_to('Beneficiario', beneficiary.id)
            contract = self.contract.get_by_id(contract_assignment.id_contrato) if contract_assignment else {}

            department = self.department.get_by_id(beneficiary.departament) if beneficiary.departament else {}
            municipality = self.municipality.get_by_id(beneficiary.municipality) if beneficiary.municipality else {}

            return structure_budget_data(budget, beneficiary, contract_assignment, contract, department, municipality, documents)

        except Exception as e:
            raise e
    
    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None):
        try:
            user = getattr(request, "user", None)
            budgets, total = self.repository.get_all_with_relationships(limit, offset, order_by, filters,user)

            results = []

            for budget in budgets:
                beneficiary = self.beneficiary.get_by_id(budget.beneficiary_id)

                contract_assignment = None
                contract = None
                department = None
                municipality = None

                if beneficiary:
                    contract_assignment = self.contract_assignment.get_by_associate_id_and_associate_to('Beneficiario', beneficiary.id)
                    department = self.department.get_by_id(beneficiary.departament) if beneficiary.departament else None
                    municipality = self.municipality.get_by_id(beneficiary.municipality) if beneficiary.municipality else None
                    diagnostic= self.diagnostic.get_by_beneficiary_id(beneficiary.id)
                    documents=[]
                    if diagnostic:
                        documents=  self.documents.get_by_associate_and_document_types([300,400], 'Diagnostic', diagnostic.id)
                    if contract_assignment:
                        contract = self.contract.get_by_id(contract_assignment.id_contrato)

                data = structure_budget_data(budget, beneficiary, contract_assignment, contract, department, municipality,documents)
                results.append(data)

            return results, total

        except Exception as e:
            raise Exception(f"Error al obtener los presupuestos: {str(e)}")


    def update_budgets_and_state(self, budget_ids: list, status_id: int, user_id: int):
        try:
            if not status_id:
                raise ValueError("status_id is required")
            if not budget_ids or not isinstance(budget_ids, list):
                raise ValueError("budget_ids must be a non-empty list")
            if not user_id:
                raise ValueError("user_id is required")

            not_updated = []

            for item in budget_ids:
                updated = self.repository.update(item, {"status_id": status_id})
                if not updated:
                    not_updated.append(item)

                budget_states_change = {
                    "budget_id": item,
                    "status_id": status_id,
                    "user_id": user_id
                }
                self.status_change.create(budget_states_change)

            return {
                "message": "Budgets updated successfully",
                "not_updated": not_updated
            }
        except Exception as e:
            raise Exception(f"Error al obtener los presupuestos: {str(e)}")

        
    def get_max_end_date_from_budget(budget):
        max_end_date = 0
        for category in budget.categories:
            for subcategory in category.subcategories:
                if subcategory.timeline and subcategory.timeline.end_date:
                    max_end_date = max(max_end_date, subcategory.timeline.end_date)
        return max_end_date
