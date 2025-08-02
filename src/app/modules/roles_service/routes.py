from fastapi import APIRouter
from app.modules.roles_service.routes.rol_routes import router as rol_routes

router = APIRouter(prefix="/roles", tags=["roles"])

router.include_router(rol_routes) 