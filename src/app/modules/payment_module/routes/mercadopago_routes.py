from fastapi import APIRouter, Depends, status, HTTPException,Request
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
    db: AsyncSession = Depends(get_db)
):
    try:
        service = MercadoPagoService(db)
        payment = await service.create_payment(data)
        return http_response(message="Payment created successfully", data=payment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook", status_code=200)
async def mercado_pago_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        body = await request.json()
        query_params = dict(request.query_params)

        service = MercadoPagoService(db)
        await service.handle_webhook(body, query_params)

        return {"message": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))