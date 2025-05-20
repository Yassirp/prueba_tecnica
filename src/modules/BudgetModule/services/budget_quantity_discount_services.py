from services.base_services import BaseService
from sqlalchemy.orm import Session
from modules.BudgetModule.repositories.budget_quantity_discount_repository import BudgetQuantityDiscountRepository
from modules.BudgetModule.models.o_budget_quantity_discounts import OBudgetQuantityDiscount
from modules.BudgetModule.schemas.budget_quantity_discount_schema import BudgetQuantityDiscountCreate, BudgetQuantityDiscountUpdate
from utils.serialize import serialize_model

class BudgetQuantityDiscountService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.repository = BudgetQuantityDiscountRepository(db)
        super().__init__(OBudgetQuantityDiscount, self.repository, BudgetQuantityDiscountCreate, BudgetQuantityDiscountUpdate)



    def create_data(self,data: list,  budget_detail_id: int):
        try:
            data_response=[]
            total=0
            for item in data:
                if not isinstance(item, dict):
                    print("ERROR: Item no es un dict:", item)  # O usa logging
                    raise TypeError("Se esperaba un diccionario en 'data', pero se recibió: " + str(type(item)))
                item_payload = {
                    "budget_quantity_detail_id": budget_detail_id,
                    "element": item.get("element"),
                    "height": item.get("height"),
                    "width": item.get("width"),
                    "length": item.get("length"),
                    "quantity": item.get("quantity"),
                    "subtotal": item.get("subtotal")
                }

                total += item.get("subtotal")
                
                i = self.create(item_payload)
                data_response.append(serialize_model(i))
            

            return data_response, total
        
        except Exception as e:
            raise e