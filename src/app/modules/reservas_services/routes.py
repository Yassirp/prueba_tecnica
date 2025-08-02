from fastapi import APIRouter
from app.modules.reservas_services.routes.reserva_routes import router as reserva_routes

router = APIRouter(prefix="/reservas", tags=["reservas"])

router.include_router(reserva_routes) 