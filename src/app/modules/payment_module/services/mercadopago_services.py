from src.app.shared.constants.settings import Settings
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.models.living_group import LivingGroup
import mercadopago
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.config.database.session import get_db
from fastapi import Depends,HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(Settings.MERCADO_PAGO_TOKEN)
        

    async def create_payment(self, data: dict):
        try:

            payment_data = {
                "items": [
                    {
                        "title": data.get("title"),
                        "quantity": 1,
                        "unit_price": data.get("amount")
                    }
                ],
                "back_urls": {
                    "success": "https://www.micro-lvr.com/success",
                    "failure": "https://www.micro-lvr.com/failure",
                    "pending": "https://www.micro-lvr.com/pending"
                },
                "auto_return": "approved",
                "payment_method_id": {
                    "excluded_payment_methods": [
                        {
                            "id": "ticket"
                        }
                    ],
                    "installments": 1,
                },
                "redirectMode": "modal",
                
            }

            result = self.sdk.preference().create(payment_data)
            return result["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
