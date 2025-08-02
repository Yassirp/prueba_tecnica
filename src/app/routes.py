from fastapi import APIRouter

from app.modules.dashboard_module.routes.booking_routes import router as booking_routes
from app.modules.dashboard_module.routes.user_routes import router as user_routes
from app.modules.soccer_field_module.routes.soccer_field_routes import router as soccer_field_routes
from app.modules.microservicio_auth.routes import router as auth_routes
from app.modules.reservas_services.routes import router as reservas_routes
from app.modules.roles_service.routes import router as roles_routes

router = APIRouter()

router.include_router(soccer_field_routes)
router.include_router(booking_routes)
router.include_router(user_routes)
router.include_router(auth_routes)
router.include_router(reservas_routes)
router.include_router(roles_routes)
