from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.ubication_module.schemas.country_schemas import CountryCreate, CountryUpdate
from src.app.modules.ubication_module.services.country_services import CountryService
from typing import Dict
from src.app.shared.utils.request_utils import  http_response, get_filter_params, paginated_response
from src.app.middleware.api_auth import require_auth, User 
from src.app.modules.payment_module.services.mercadopago_services import MercadoPagoService

router = APIRouter(prefix="/mercadopago", tags=["MercadoPago"])


@router.post("/create-preference", status_code=status.HTTP_200_OK)
async def create_payment(
    data: dict,

):
    try:
        service = MercadoPagoService()
        payment = await service.create_payment(data)
        return http_response(message="Payment created successfully", data=payment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
