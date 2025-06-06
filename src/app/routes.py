from fastapi import APIRouter
from .modules.parameters_module.routes.parameters_routes import router as parameters_routes
from .modules.attributes_module.routes.attributes_routes import router as attributes_routes
from .modules.projects_module.routes.projects_routes import router as projects_router
from .modules.document_rules_module.routes.document_rules_routes import router as document_rules_routes
from .modules.entity_documents_module.routes.entity_documents_routes import router as entity_documents_routes
from .modules.entity_types_module.routes.entity_type_routes import (
    router as entity_types_router,
)
from .modules.notifications_module.routes.notifications_routes import router as notifications_routes
from .modules.entity_document_logs_module.routes.entity_document_logs_routes import router as entity_document_logs_routes
from .modules.access_tokens_module.routes.access_tokens_routes import router as access_tokens_routes
router = APIRouter()

router.include_router(projects_router)
router.include_router(entity_types_router)
router.include_router(parameters_routes)
router.include_router(attributes_routes)
router.include_router(document_rules_routes)
router.include_router(entity_documents_routes)
router.include_router(entity_document_logs_routes)
router.include_router(notifications_routes)
router.include_router(access_tokens_routes)