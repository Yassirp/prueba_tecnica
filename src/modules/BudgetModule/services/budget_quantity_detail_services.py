from services.base_services import BaseService
from sqlalchemy.orm import Session
from modules.BudgetModule.repositories.budget_quantity_detail_repository import BudgetQuantityDetailRepository
from modules.BudgetModule.models.o_budget_quantity_details import OBudgetQuantityDetail
from modules.BudgetModule.services.budget_quantity_discount_services import BudgetQuantityDiscountService
from modules.BudgetModule.services.budget_quantity_total_services import BudgetQuantityTotalService
from modules.BudgetModule.schemas.budget_quantity_detail_schema import BudgetQuantityDetailCreate, BudgetQuantityDetailUpdate
from utils.serialize import serialize_model

class BudgetQuantityDetailService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.repository = BudgetQuantityDetailRepository(db)
        self.budget_quantity_discount = BudgetQuantityDiscountService(db)
        self.budget_quantity_total = BudgetQuantityTotalService(db)
        super().__init__(OBudgetQuantityDetail, self.repository, BudgetQuantityDetailCreate, BudgetQuantityDetailUpdate)



    def create_data(self,budget_subcategory_id: int, data: list):
        try:
            data_response = {
                "budget_quantity": [],
                "budget_quantity_discount": []
            }

            for item in data:
                if not isinstance(item, dict):
                    print("ERROR: Item no es un dict:", item)  # O usa logging
                    raise TypeError("Se esperaba un diccionario en 'data', pero se recibió: " + str(type(item)))

                total = 0

                item_payload = {
                    "budget_subcategory_id": budget_subcategory_id,
                    "location": item.get("location"),
                    "height": item.get("height"),
                    "width": item.get("width"),
                    "length": item.get("length"),
                    "quantity": item.get("quantity"),
                    "subtotal": item.get("subtotal"),
                }
                total += item.get("subtotal")
                i = self.create(item_payload)
                if not getattr(i, "id", None):
                    raise Exception("No se pudo obtener el ID del detalle de cantidad presupuestal.")
                data_response["budget_quantity"].append(serialize_model(i))

                if item.get("discounts"):  
                    discount, total_rest = self.budget_quantity_discount.create_data(item.get("discounts"), i.id)
                    total -= total_rest
                    data_response["budget_quantity_discount"].append(discount)

                total_data = item.get("total", {"total": total})
                total_data["budget_quantity_detail_id"] = i.id
                self.budget_quantity_total.create(total_data)

            return data_response  

        except Exception as e:
            raise e

            
    def update_data(self, budget_data: list):
        pass
        
