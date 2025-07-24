from src.app.shared.constants.settings import Settings
from datetime import datetime
import uuid
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.models.living_group import LivingGroup
import mercadopago
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.config.database.session import get_db
from fastapi import HTTPException
from src.app.modules.payment_module.repositories.payment_repository import PaymentRepository
from src.app.modules.payment_module.models.payment import Payment
from src.app.modules.user_module.services.user_service import UserService


class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(Settings.MERCADO_PAGO_TOKEN)
        self.payment_repository = PaymentRepository(Payment, get_db())
        self.living_group_repository = LivingGroupRepository(LivingGroup, get_db())

    async def create_payment(self, data: dict):
        try:
            living_group = await self.living_group_repository.get_by_id(data.get("living_group_id"))
            if not living_group:
                raise HTTPException(status_code=404, detail="Grupo de vida no encontrado")

            external_reference = living_group.id + "_" + str(datetime.now().timestamp()) + "_" + str(uuid.uuid4())
            
            payment_data = {
                "items": [
                    {
                        "title": living_group.name,
                        "quantity": 1,
                        "unit_price": living_group.value
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
                "external_reference": external_reference,
                "redirectMode": "modal"
            }

            result = self.sdk.preference().create(payment_data)
            data_create={
                "living_group_id": living_group.id,
                "pasarela":"mercadopago",
                "payment_id": result["response"]["id"],
                "payment_status": result["response"]["status"],
                "amount": living_group.value,
                "data": data["user_data"],
                "external_reference": external_reference
            }
            await self.payment_repository.create(data_create)
            return result["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def handle_webhook(self, body: dict, query_params: dict):
        topic = query_params.get("topic")
        payment_id = query_params.get("id")

        if topic != "payment":
            raise HTTPException(status_code=400, detail="Evento no válido")

        payment = self.sdk.payment().get(payment_id)

        payment_status = payment["response"]["status"]
        external_reference = payment["response"].get("external_reference")

        if external_reference:
            payment = await self.payment_repository.get_by_external_reference(external_reference)

            if not payment:
                raise HTTPException(status_code=404, detail="Grupo no encontrado")

            payment.payment_status = payment_status
            await self.payment_repository.update(payment)
            
            if payment_status == "approved":
                user_service = UserService(get_db())
                await user_service.register(payment.data)
                return {"message": "Pago aprobado"}