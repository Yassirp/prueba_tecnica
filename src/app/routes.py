from fastapi import APIRouter
from src.app.modules.user_module.routes.user_routes import router as user_routes
from src.app.modules.document_module.routes.document_routes import router as document_routes
router = APIRouter()

router.include_router(user_routes)
router.include_router(document_routes)