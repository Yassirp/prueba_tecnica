from app.shared.constants.settings import Settings
from app.modules.living_group_module.services.living_group_service import LivingGroupService
import mercadopago
from sqlalchemy.orm import Session
from app.modules.living_group_module.models.living_group import LivingGroup
from src.app.config.database.session import get_db
from fastapi import Depends,HTTPException

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(Settings.MERCADO_PAGO_TOKEN)
        self.living_group_service = LivingGroupService(db_session=Depends(get_db))

    async def create_payment(self, payment_data):
        living_group_id = payment_data.get("living_group_id")
        back_urls = payment_data.get("back_urls")
        if not back_urls:
            raise HTTPException(status_code=400, detail="Back URLs are required")
        living_group = await self.living_group_service.get_by_id(living_group_id)
        if not living_group:
            raise HTTPException(status_code=404, detail="Living group not found")
        
        preference_data = {
            "items": [
                {
                    "title": living_group["name"],
                    "quantity": 1,
                    "unit_price": living_group["value"],
                }
            ],
            "back_urls": back_urls,
            "auto_return": payment_data.get("auto_return") or "approved",
            "binary_mode": True,
            "notification_url": "https://www.micro-lvr.com/notifications",
            "metadata": {
                "living_group_id": living_group_id
            }
        }
        preference_response = self.sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        return preference