from fastapi import APIRouter
from src.app.modules.user_module.routes.user_routes import router as user_routes
from src.app.modules.document_module.routes.document_routes import router as document_routes
from src.app.modules.user_module.routes.user_relationship_routes import router as user_relationship_routes
from src.app.modules.parameters_module.routes.parameters_routes import router as parameters_routes
from src.app.modules.ubication_module.routes.contry_routes import router as country_routes
from src.app.modules.permission_module.routes.role_routes import router as role_routes
from src.app.modules.user_module.routes.report_routes import router as report_routes 
from src.app.modules.sedes_module.routes.sedes_routes import router as sedes_routes
from src.app.modules.living_group_module.routes.living_group_routes import router as living_group_routes
from src.app.modules.living_group_module.routes.living_group_user_routes import router as living_group_user_routes
from src.app.modules.payment_module.routes.mercadopago_routes import router as mercado_pago_routes
router = APIRouter()

router.include_router(user_routes)
router.include_router(document_routes)
router.include_router(user_relationship_routes)
router.include_router(parameters_routes)
router.include_router(country_routes)
router.include_router(role_routes)
router.include_router(report_routes)
router.include_router(sedes_routes)
router.include_router(living_group_routes)
router.include_router(living_group_user_routes)
router.include_router(mercado_pago_routes)