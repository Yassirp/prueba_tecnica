from fastapi import APIRouter
from .modules.projects_module.routes.projects_routes import router as projects_router
from .modules.entity_types_module.routes.entity_type_routes import (
    router as entity_types_router,
)

router = APIRouter()

router.include_router(projects_router)
router.include_router(entity_types_router)
