from fastapi import APIRouter
from src.app.modules.user_module.routes.user_routes import router as user_routes
router = APIRouter()

router.include_router(user_routes)
