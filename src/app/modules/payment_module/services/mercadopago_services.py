from src.app.shared.constants.settings import Settings
from datetime import datetime
import uuid
from src.app.modules.living_group_module.repositories.living_group_repository import LivingGroupRepository
from src.app.modules.living_group_module.models.living_group import LivingGroup
import mercadopago
from src.app.modules.living_group_module.models.living_group import LivingGroup
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.app.modules.payment_module.repositories.payment_repository import PaymentRepository
from src.app.modules.payment_module.models.payment import Payment
from src.app.modules.user_module.services.user_service import UserService
from src.app.utils.domain_api import get_domain_api
from src.app.modules.user_module.repositories.user_repository import UserRepository
from src.app.modules.user_module.models.users import User
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MercadoPagoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sdk = mercadopago.SDK(Settings.MERCADO_PAGO_TOKEN)
        self.payment_repository = PaymentRepository(Payment, db)
        self.user_repository = UserRepository(User, db)
        self.living_group_repository = LivingGroupRepository(LivingGroup, db)

    async def create_payment(self, data: dict):
        try:
            living_group = await self.living_group_repository.get_by_id(data.get("living_group_id"))
            if not living_group:
                raise HTTPException(status_code=404, detail="Grupo de vida no encontrado")
            domain = get_domain_api()
            external_reference = f"{living_group.id}_{datetime.now().timestamp()}_{uuid.uuid4()}"
            user = await self.user_repository.get_by_email(data.get("email"))
            if user:
                raise HTTPException(status_code=400, detail="email registrado, por favor intente con otro email")
            
            payment_data = {
                "items": [
                    {
                        "title": living_group.name,
                        "quantity": 1,
                        "unit_price": float(living_group.value)
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
                "redirectMode": "modal",
                "notification_url": f"{domain}/mercadopago/webhook",
                "payer":{
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "phone": {
                        "area_code": "+57",
                        "number": data.get("phone_number")
                    },
                    "identification":{
                        "number": data.get("document_number")
                    }
                }
            }

            result = self.sdk.preference().create(payment_data)
            print("RESULTADO MERCADOPAGO:", result)
            print("RESPONSE:", result.get("response"))
            response = result.get("response", {})

            data_create={
                "living_group_id": living_group.id,
                "pasarela":"mercadopago",
                "payment_id": response["id"],
                "payment_status": "pending",
                "amount": float(living_group.value),
                "data": data["data"],
                "external_reference": external_reference
            }
            await self.payment_repository.create(data_create)
            return result["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def handle_webhook(self, body: dict, query_params: dict):
        topic = query_params.get("topic")
        payment_id = query_params.get("id")
        password = query_params.get("password")
        logger.info(f"Webhook recibido: {body}")
        logger.info(f"Query params: {query_params}")
        logger.info(f"Password: {password}")
        if password != Settings.MERCADO_PAGO_WEBHOOK_PASSWORD:
            raise HTTPException(status_code=403, detail="Acceso no autorizado")
        if topic != "payment":
            raise HTTPException(status_code=400, detail="Evento no válido")

        payment = self.sdk.payment().get(payment_id)
        logger.info(f"Payment: {payment}")
        payment_status = payment["response"]["status"]
        external_reference = payment["response"].get("external_reference")

        if external_reference:
            logger.info(f"External reference: {external_reference}")
            payment = await self.payment_repository.get_by_external_reference(external_reference)
            logger.info(f"Payment: {payment}")
            if not payment:
                raise HTTPException(status_code=404, detail="Grupo no encontrado")

            payment.payment_status = payment_status
            logger.info(f"Payment status: {payment_status}")
            await self.payment_repository.update(payment)
            logger.info(f"Payment updated: {payment}")
            if payment_status == "approved":
                user_service = UserService(self.db)
                await user_service.register(payment.data)
                logger.info(f"User registered: {payment.data}")
                return {"message": "Pago aprobado"}