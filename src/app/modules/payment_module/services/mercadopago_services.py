from src.app.shared.constants.settings import Settings
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.models.living_group import LivingGroup
import mercadopago
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.config.database.session import get_db
from fastapi import Depends,HTTPException
from src.app.modules.payment_module.repositories.payment_repository import PaymentRepository
from src.app.modules.payment_module.models.payment import Payment

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(Settings.MERCADO_PAGO_TOKEN)
        self.payment_repository = PaymentRepository(Payment, get_db())
        

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
                "notification_url": "https://www.micro-lvr.com/notification",
            }

            result = self.sdk.preference().create(payment_data)
            data_create={
                "living_group_id": data.get("living_group_id"),
                "pasarela":"mercadopago",
                "payment_id": result["response"]["id"],
                "payment_status": result["response"]["status"],
                "amount": data.get("amount"),
                "data": data["user_data"]
            }
            await self.payment_repository.create(data_create)
            return result["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
