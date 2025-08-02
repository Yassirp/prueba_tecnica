from fastapi import APIRouter
from app.modules.microservicio_auth.routes.auth_routes import router as auth_routes

router = APIRouter(prefix="/auth", tags=["authentication"])

router.include_router(auth_routes) 