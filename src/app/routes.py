from fastapi import APIRouter
from src.app.modules.user_module.routes.user_routes import router as user_routes
from src.app.modules.document_module.routes.document_routes import router as document_routes
from src.app.modules.user_module.routes.user_relationship_routes import router as user_relationship_routes
from src.app.modules.parameters_module.routes.parameters_routes import router as parameters_routes
from src.app.modules.ubication_module.routes.contry_routes import router as country_routes
from src.app.modules.permission_module.routes.role_routes import router as role_routes
router = APIRouter()

router.include_router(user_routes)
router.include_router(document_routes)
router.include_router(user_relationship_routes)
router.include_router(parameters_routes)
router.include_router(country_routes)
router.include_router(role_routes)