from modules.ParameterModule.models.m_parameters_values import MParameterValue
from modules.ParameterModule.schemas.parameter_value_schema import MParameterValueCreate, MParameterValueUpdate
from modules.ParameterModule.repositories.pv_repository import ParameterValueRepository
from services.base_services import BaseService
# from utils.serialize import
class ParameterValueService(BaseService):
    def __init__(self, db):
        self.db = db
        self.repo = ParameterValueRepository(db)
        super().__init__(
            MParameterValue,
            self.repo,
            MParameterValueCreate,
            MParameterValueUpdate
        )
        
 
    def get_parameter_value_by_parameter_reference(self, references: list):
        
        data= {}
        for ref in references:
            services = self.repo.get_by_parameter_reference(ref)
            data[ref] = []  # Initialize an empty list for each reference
            for item in services:
                data[ref].append({
                    "id": item.id,
                    "reference": item.reference,
                    "description": item.description,
                    "value": item.value
                })
        
        if not data:
          return None
      
        return data 

            
            
        